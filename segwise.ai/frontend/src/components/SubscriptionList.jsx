import { useState, useEffect } from 'react';
import { Box, Table, Thead, Tbody, Tr, Th, Td, Button, Badge, useToast } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';
import axios from 'axios';

function SubscriptionList() {
  const [subscriptions, setSubscriptions] = useState([]);
  const toast = useToast();

  useEffect(() => {
    fetchSubscriptions();
  }, []);

  const fetchSubscriptions = async () => {
    try {
      const response = await axios.get('http://localhost:8000/subscriptions/');
      setSubscriptions(response.data);
    } catch (error) {
      toast({
        title: 'Error fetching subscriptions',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const toggleSubscriptionStatus = async (id, currentStatus) => {
    try {
      await axios.put(`http://localhost:8000/subscriptions/${id}`, {
        is_active: !currentStatus
      });
      fetchSubscriptions();
      toast({
        title: 'Subscription updated',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error updating subscription',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box overflowX="auto">
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>ID</Th>
            <Th>Target URL</Th>
            <Th>Event Types</Th>
            <Th>Status</Th>
            <Th>Created At</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {subscriptions.map((subscription) => (
            <Tr key={subscription.id}>
              <Td>{subscription.id}</Td>
              <Td>{subscription.target_url}</Td>
              <Td>
                {subscription.event_types?.map((type) => (
                  <Badge key={type} mr={2} colorScheme="blue">
                    {type}
                  </Badge>
                ))}
              </Td>
              <Td>
                <Badge
                  colorScheme={subscription.is_active ? 'green' : 'red'}
                >
                  {subscription.is_active ? 'Active' : 'Inactive'}
                </Badge>
              </Td>
              <Td>{new Date(subscription.created_at).toLocaleString()}</Td>
              <Td>
                <Button
                  as={RouterLink}
                  to={`/subscriptions/${subscription.id}/logs`}
                  size="sm"
                  colorScheme="blue"
                  mr={2}
                >
                  View Logs
                </Button>
                <Button
                  size="sm"
                  colorScheme={subscription.is_active ? 'red' : 'green'}
                  onClick={() => toggleSubscriptionStatus(subscription.id, subscription.is_active)}
                >
                  {subscription.is_active ? 'Deactivate' : 'Activate'}
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
}

export default SubscriptionList;