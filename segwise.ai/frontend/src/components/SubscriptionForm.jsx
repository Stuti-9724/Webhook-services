import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  useToast,
  Tag,
  TagLabel,
  TagCloseButton,
  HStack,
  Switch,
  FormHelperText,
} from '@chakra-ui/react';
import axios from 'axios';

function SubscriptionForm() {
  const navigate = useNavigate();
  const toast = useToast();
  const [formData, setFormData] = useState({
    target_url: '',
    secret_key: '',
    event_types: [],
    is_active: true,
  });
  const [newEventType, setNewEventType] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/subscriptions/', formData);
      toast({
        title: 'Subscription created',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      navigate('/');
    } catch (error) {
      toast({
        title: 'Error creating subscription',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleAddEventType = (e) => {
    if (e.key === 'Enter' && newEventType) {
      e.preventDefault();
      if (!formData.event_types.includes(newEventType)) {
        setFormData({
          ...formData,
          event_types: [...formData.event_types, newEventType],
        });
      }
      setNewEventType('');
    }
  };

  const handleRemoveEventType = (eventType) => {
    setFormData({
      ...formData,
      event_types: formData.event_types.filter((type) => type !== eventType),
    });
  };

  return (
    <Box maxW="container.md" mx="auto">
      <form onSubmit={handleSubmit}>
        <VStack spacing={4} align="stretch">
          <FormControl isRequired>
            <FormLabel>Target URL</FormLabel>
            <Input
              type="url"
              value={formData.target_url}
              onChange={(e) =>
                setFormData({ ...formData, target_url: e.target.value })
              }
              placeholder="https://example.com/webhook"
            />
          </FormControl>

          <FormControl>
            <FormLabel>Secret Key</FormLabel>
            <Input
              type="text"
              value={formData.secret_key}
              onChange={(e) =>
                setFormData({ ...formData, secret_key: e.target.value })
              }
              placeholder="Optional: Enter a secret key for signature verification"
            />
          </FormControl>

          <FormControl>
            <FormLabel>Event Types</FormLabel>
            <Input
              value={newEventType}
              onChange={(e) => setNewEventType(e.target.value)}
              onKeyDown={handleAddEventType}
              placeholder="Type event name and press Enter"
            />
            <FormHelperText>
              Press Enter to add event types (e.g., user.created, order.updated)
            </FormHelperText>
            <HStack spacing={2} mt={2} wrap="wrap">
              {formData.event_types.map((type) => (
                <Tag
                  key={type}
                  size="md"
                  borderRadius="full"
                  variant="solid"
                  colorScheme="blue"
                >
                  <TagLabel>{type}</TagLabel>
                  <TagCloseButton
                    onClick={() => handleRemoveEventType(type)}
                  />
                </Tag>
              ))}
            </HStack>
          </FormControl>

          <FormControl display="flex" alignItems="center">
            <FormLabel htmlFor="is-active" mb="0">
              Active
            </FormLabel>
            <Switch
              id="is-active"
              isChecked={formData.is_active}
              onChange={(e) =>
                setFormData({ ...formData, is_active: e.target.checked })
              }
            />
          </FormControl>

          <Button type="submit" colorScheme="blue">
            Create Subscription
          </Button>
        </VStack>
      </form>
    </Box>
  );
}

export default SubscriptionForm;