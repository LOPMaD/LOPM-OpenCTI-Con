import sys
from datetime import datetime, timezone

from pycti import OpenCTIConnectorHelper, get_config_variable
from LopmConnectorClient import LopmConnectorClient    
from LopmConverterToStix import LopmConverterToStix

class LopmConnector:

    def __init__(self, config):

        self.config = config
        
        self.helper = OpenCTIConnectorHelper(config=config)

        self.client = LopmConnectorClient()

        self.converter_to_stix = LopmConverterToStix(
            self.helper,
            tlp_level=get_config_variable("TLP_LEVEL", ['lopmconnector', 'tlp_level'], self.config),
        )
    
       


     

    def _collect_intelligence(self) -> list:

        # Collect intelligence from the source and convert into STIX object
        # :return: List of STIX objects

        stix_objects = []

        stix_package_container = []
        # Get entities from external sources
        entities = self.client.get_entities()
        
        i = 1
        j = 0
        for entity in entities:
            print("Перетворено доменів у stix:", i, " Кількість пакетів:", j)
            entity_to_stix = self.converter_to_stix.create_obs(entity)
            i += 1
            stix_objects.append(entity_to_stix)
            if len(stix_objects) == 500:
                stix_objects.append(self.converter_to_stix.author)
                stix_objects.append(self.converter_to_stix.tlp_marking)
                
                stix_package_container.append(stix_objects)
                
                stix_objects = []
                
                i = 1
                j += 1


       
        if len(stix_objects):
            stix_objects.append(self.converter_to_stix.author)
            stix_objects.append(self.converter_to_stix.tlp_marking)

            stix_package_container.append(stix_objects)

        return stix_package_container

    def process_message(self) -> None:
        
        # Connector main process to collect intelligence
        # :return: None
        
        self.helper.connector_logger.info(
            "[CONNECTOR] Starting connector...",
            {"connector_name": self.helper.connect_name},
        )

        try:
            # Get the current state
            now = datetime.now()
            current_timestamp = int(datetime.timestamp(now))
            current_state = self.helper.get_state()

            if current_state is not None and "last_run" in current_state:
                last_run = current_state["last_run"]

                self.helper.connector_logger.info(
                    "[CONNECTOR] Connector last run",
                    {"last_run_datetime": last_run},
                )
            else:
                self.helper.connector_logger.info(
                    "[CONNECTOR] Connector has never run..."
                )

            # Friendly name will be displayed on OpenCTI platform
            friendly_name = "LOPM feed"

            # Initiate a new work

            work_id = self.helper.api.work.initiate_work(
                self.helper.connect_id, friendly_name
            )

            self.helper.connector_logger.info(
                "[CONNECTOR] Running connector...",
                {"connector_name": self.helper.connect_name},
            )

            # Performing the collection of intelligence 



            stix_package_container = self._collect_intelligence()
            for stix_objects in stix_package_container:
                if len(stix_objects):
                    # work_id = self.helper.api.work.initiate_work(
                    #     self.helper.connect_id, friendly_name
                    # )
                    
                    stix_objects_bundle = self.helper.stix2_create_bundle(stix_objects)

                    bundles_sent = self.helper.send_stix2_bundle(
                        bundle=stix_objects_bundle,
                        work_id=work_id,
                        cleanup_inconsistent_bundle=True,
                    )

                    self.helper.connector_logger.info(
                        "Sending STIX objects to OpenCTI...",
                        {"bundles_sent": {str(len(bundles_sent))}},
                    )
                

            # Store the current timestamp as a last run of the connector
            self.helper.connector_logger.debug(
                "Getting current state and update it with last run of the connector",
                {"current_timestamp": current_timestamp},
            )
            current_state = self.helper.get_state()
            current_state_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
            last_run_datetime = datetime.fromtimestamp(
                current_timestamp, tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S")
            if current_state:
                current_state["last_run"] = current_state_datetime
            else:
                current_state = {"last_run": current_state_datetime}
            self.helper.set_state(current_state)

            
            message = (
                f"{self.helper.connect_name} connector successfully run, storing last_run as "
                + str(last_run_datetime)
            )
        
            self.helper.api.work.to_processed(work_id, message)
            self.helper.connector_logger.info(message)

        except (KeyboardInterrupt, SystemExit):
            self.helper.connector_logger.info(
                "[CONNECTOR] Connector stopped...",
                {"connector_name": self.helper.connect_name},
            )
            sys.exit(0)
        except Exception as err:
            self.helper.connector_logger.error(str(err))

    def run(self) -> None:
        # Start the connector, schedule its runs and trigger the first run.
        # It allows you to schedule the process to run at a certain interval.
        # This specific scheduler from the `OpenCTIConnectorHelper` will also check the queue size of a connector.
        # If `CONNECTOR_QUEUE_THRESHOLD` is set, and if the connector's queue size exceeds the queue threshold,
        # the connector's main process will not run until the queue is ingested and reduced sufficiently,
        # allowing it to restart during the next scheduler check. (default is 500MB)

        # Example:
        #     - If `CONNECTOR_DURATION_PERIOD=PT5M`, then the connector is running every 5 minutes.
        print("Good?")
        self.helper.schedule_process(
            message_callback=self.process_message,
            duration_period=86400,
        )
        print("GoodJOBJOB???")

