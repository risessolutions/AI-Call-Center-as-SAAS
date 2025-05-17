import unittest
from unittest.mock import MagicMock, patch
from src.integrations.integration_manager import IntegrationManager, SalesforceIntegration, HubSpotIntegration

class TestIntegrationManager(unittest.TestCase):
    """Test cases for Integration Manager."""
    
    def setUp(self):
        """Set up test environment."""
        self.integration_manager = IntegrationManager()
        
        # Mock the connect method for all integration types
        for integration_class in self.integration_manager.integration_types.values():
            integration_class.connect = MagicMock(return_value=True)
            integration_class.disconnect = MagicMock(return_value=True)
            integration_class.test_connection = MagicMock(return_value={"success": True})
    
    def test_add_integration(self):
        """Test adding an integration."""
        # Add Salesforce integration
        result = self.integration_manager.add_integration("salesforce", {
            "username": "test@example.com",
            "password": "password",
            "security_token": "token",
            "domain": "test.salesforce.com"
        })
        
        # Verify result
        self.assertTrue(result["success"])
        self.assertIn("integration_id", result)
        self.assertEqual(result["status"]["name"], "Salesforce")
        self.assertEqual(result["status"]["type"], "crm")
        self.assertEqual(result["status"]["status"], "active")
        
        # Verify integration was added
        integration_id = result["integration_id"]
        self.assertIn(integration_id, self.integration_manager.integrations)
        
        # Verify connect was called
        integration = self.integration_manager.integrations[integration_id]
        integration.connect.assert_called_once()
    
    def test_add_unknown_integration(self):
        """Test adding an unknown integration type."""
        result = self.integration_manager.add_integration("unknown", {})
        
        # Verify result
        self.assertFalse(result["success"])
        self.assertIn("message", result)
    
    def test_remove_integration(self):
        """Test removing an integration."""
        # First add an integration
        result = self.integration_manager.add_integration("salesforce", {})
        integration_id = result["integration_id"]
        
        # Now remove it
        success = self.integration_manager.remove_integration(integration_id)
        
        # Verify result
        self.assertTrue(success)
        self.assertNotIn(integration_id, self.integration_manager.integrations)
        
        # Verify disconnect was called
        integration = result["status"]
        self.integration_manager.integration_types["salesforce"].disconnect.assert_called_once()
    
    def test_remove_unknown_integration(self):
        """Test removing an unknown integration."""
        success = self.integration_manager.remove_integration("unknown")
        
        # Verify result
        self.assertFalse(success)
    
    def test_get_integration(self):
        """Test getting an integration."""
        # First add an integration
        result = self.integration_manager.add_integration("salesforce", {})
        integration_id = result["integration_id"]
        
        # Now get it
        integration = self.integration_manager.get_integration(integration_id)
        
        # Verify result
        self.assertIsNotNone(integration)
        self.assertEqual(integration.name, "Salesforce")
    
    def test_get_unknown_integration(self):
        """Test getting an unknown integration."""
        integration = self.integration_manager.get_integration("unknown")
        
        # Verify result
        self.assertIsNone(integration)
    
    def test_get_integrations(self):
        """Test getting all integrations."""
        # Add two integrations
        result1 = self.integration_manager.add_integration("salesforce", {})
        result2 = self.integration_manager.add_integration("hubspot", {})
        
        # Get all integrations
        integrations = self.integration_manager.get_integrations()
        
        # Verify result
        self.assertEqual(len(integrations), 2)
        self.assertIn(result1["integration_id"], integrations)
        self.assertIn(result2["integration_id"], integrations)
    
    def test_get_integrations_by_type(self):
        """Test getting integrations by type."""
        # Add two integrations
        result1 = self.integration_manager.add_integration("salesforce", {})
        result2 = self.integration_manager.add_integration("hubspot", {})
        
        # Get CRM integrations
        integrations = self.integration_manager.get_integrations("crm")
        
        # Verify result
        self.assertEqual(len(integrations), 2)
        self.assertIn(result1["integration_id"], integrations)
        self.assertIn(result2["integration_id"], integrations)
        
        # Get ERP integrations
        integrations = self.integration_manager.get_integrations("erp")
        
        # Verify result
        self.assertEqual(len(integrations), 0)
    
    def test_test_integration(self):
        """Test testing an integration."""
        # First add an integration
        result = self.integration_manager.add_integration("salesforce", {})
        integration_id = result["integration_id"]
        
        # Now test it
        test_result = self.integration_manager.test_integration(integration_id)
        
        # Verify result
        self.assertTrue(test_result["success"])
        
        # Verify test_connection was called
        integration = self.integration_manager.integrations[integration_id]
        integration.test_connection.assert_called_once()
    
    def test_test_unknown_integration(self):
        """Test testing an unknown integration."""
        test_result = self.integration_manager.test_integration("unknown")
        
        # Verify result
        self.assertFalse(test_result["success"])
        self.assertIn("message", test_result)

class TestSalesforceIntegration(unittest.TestCase):
    """Test cases for Salesforce Integration."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = {
            "username": "test@example.com",
            "password": "password",
            "security_token": "token",
            "domain": "test.salesforce.com"
        }
        self.integration = SalesforceIntegration(self.config)
    
    def test_initialization(self):
        """Test initialization."""
        self.assertEqual(self.integration.name, "Salesforce")
        self.assertEqual(self.integration.type, "crm")
        self.assertEqual(self.integration.status, "inactive")
        self.assertEqual(self.integration.username, "test@example.com")
        self.assertEqual(self.integration.password, "password")
        self.assertEqual(self.integration.security_token, "token")
        self.assertEqual(self.integration.domain, "test.salesforce.com")
    
    @patch('src.integrations.integration_manager.logger')
    def test_connect(self, mock_logger):
        """Test connect method."""
        # Test successful connection
        success = self.integration.connect()
        
        # Verify result
        self.assertTrue(success)
        self.assertEqual(self.integration.status, "active")
        mock_logger.info.assert_called_with("Simulating Salesforce connection")
        
        # Test connection with missing credentials
        integration = SalesforceIntegration({})
        success = integration.connect()
        
        # Verify result
        self.assertFalse(success)
        mock_logger.error.assert_called_with("Missing required credentials for Salesforce")
    
    @patch('src.integrations.integration_manager.logger')
    def test_disconnect(self, mock_logger):
        """Test disconnect method."""
        # First connect
        self.integration.connect()
        
        # Now disconnect
        success = self.integration.disconnect()
        
        # Verify result
        self.assertTrue(success)
        self.assertEqual(self.integration.status, "inactive")
        self.assertIsNone(self.integration.client)
        mock_logger.info.assert_called_with("Disconnecting from Salesforce")
    
    def test_get_contacts(self):
        """Test get_contacts method."""
        # First connect
        self.integration.connect()
        
        # Get contacts
        contacts = self.integration.get_contacts()
        
        # Verify result
        self.assertEqual(len(contacts), 2)
        self.assertEqual(contacts[0]["firstName"], "John")
        self.assertEqual(contacts[1]["firstName"], "Jane")
        
        # Test when not connected
        self.integration.status = "inactive"
        contacts = self.integration.get_contacts()
        
        # Verify result
        self.assertEqual(len(contacts), 0)

if __name__ == '__main__':
    unittest.main()
