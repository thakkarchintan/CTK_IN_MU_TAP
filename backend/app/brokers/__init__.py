# Broker adapters (BrokerInterface, MockBroker, SimulationBroker, PaperBroker, KiteBroker) live here.
# KiteBroker's historical-data methods land in Step 3; order-placement methods land in Step 6.
# All Kite SDK usage must stay inside this package — strategy code must never import it directly.
