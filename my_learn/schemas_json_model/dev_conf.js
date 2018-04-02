const settings = {
  "up_dev": [
    {
      "gateway_id": "201501", 
      "dev_type": "IotGateway", 
      "nodes": [
        {
          "attributes": [
            "tem", 
            "hum"
          ], 
          "node_id": "0300110203600018"
        }, 
        {
          "attributes": [
            "tem", 
            "hum"
          ], 
          "node_id": "0300110103700025"
        }
      ], 
      "queue": {
        "routing_keys": [
          "node.0300110203600018.attributes.tem", 
          "node.0300110203600018.attributes.hum", 
          "node.0300110103700025.attributes.tem", 
          "node.0300110103700025.attributes.hum"
        ], 
        "exchange": "gateway.201501"
      }, 
      "alias": "test_gateway_201501"
    }, 
    {
      "gateway_id": "201502", 
      "dev_type": "IotGateway", 
      "nodes": [
        {
          "attributes": [
            "tem", 
            "hum"
          ], 
          "node_id": "0300110203600018"
        }, 
        {
          "attributes": [
            "tem", 
            "hum"
          ], 
          "node_id": "0300110103700025"
        }
      ], 
      "queue": {
        "routing_keys": [
          "node.0300110203600018.attributes.tem", 
          "node.0300110203600018.attributes.hum", 
          "node.0300110103700025.attributes.tem", 
          "node.0300110103700025.attributes.hum"
        ], 
        "exchange": "gateway.201502"
      }, 
      "alias": "test_gateway_201502"
    }, 
    {
      "gateway_id": "201503", 
      "dev_type": "IotGateway", 
      "nodes": [
        {
          "attributes": [
            "tem", 
            "hum"
          ], 
          "node_id": "0300110203600018"
        }, 
        {
          "attributes": [
            "tem", 
            "hum"
          ], 
          "node_id": "0300110103700025"
        }
      ], 
      "queue": {
        "routing_keys": [
          "node.0300110203600018.attributes.tem", 
          "node.0300110203600018.attributes.hum", 
          "node.0300110103700025.attributes.tem", 
          "node.0300110103700025.attributes.hum"
        ], 
        "exchange": "gateway.201503"
      }, 
      "alias": "test_gateway_201503"
    }, 
    {
      "gateway_id": "201504", 
      "dev_type": "IotGateway", 
      "nodes": [
        {
          "attributes": [
            "tem", 
            "hum"
          ], 
          "node_id": "0300110203600018"
        }, 
        {
          "attributes": [
            "tem", 
            "hum"
          ], 
          "node_id": "0300110103700025"
        }
      ], 
      "queue": {
        "routing_keys": [
          "node.0300110203600018.attributes.tem", 
          "node.0300110203600018.attributes.hum", 
          "node.0300110103700025.attributes.tem", 
          "node.0300110103700025.attributes.hum"
        ], 
        "exchange": "gateway.201504"
      }, 
      "alias": "test_gateway_201504"
    }, 
    {
      "gateway_id": "201505", 
      "dev_type": "IotGateway", 
      "nodes": [
        {
          "attributes": [
            "tem", 
            "hum"
          ], 
          "node_id": "0300110203600018"
        }, 
        {
          "attributes": [
            "tem", 
            "hum"
          ], 
          "node_id": "0300110103700025"
        }
      ], 
      "queue": {
        "routing_keys": [
          "node.0300110203600018.attributes.tem", 
          "node.0300110203600018.attributes.hum", 
          "node.0300110103700025.attributes.tem", 
          "node.0300110103700025.attributes.hum"
        ], 
        "exchange": "gateway.201505"
      }, 
      "alias": "test_gateway_201505"
    }
  ], 
  "rabbitmq_conf": {
    "host": "127.0.0.1"
  }
};

module.exports = settings;