import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  useToast,
  Heading,
  Code,
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
} from '@chakra-ui/react';
import axios from 'axios';

function WebhookLogs() {
  const { id } = useParams();
  const [logs, setLogs] = useState([]);
  const [selectedPayload, setSelectedPayload] = useState(null);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const toast = useToast();

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, [id]);

  const fetchLogs = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/subscriptions/${id}/logs`);
      setLogs(response.data);
    } catch (error) {
      toast({
        title: 'Error fetching logs',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'success':
        return 'green';
      case 'failed':
        return 'red';
      case 'pending':
        return 'yellow';
      default:
        return 'gray';
    }
  };

  const showPayload = (payload) => {
    setSelectedPayload(payload);
    onOpen();
  };

  return (
    <Box>
      <Heading size="lg" mb={6}>
        Webhook Delivery Logs
      </Heading>

      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Webhook ID</Th>
            <Th>Timestamp</Th>
            <Th>Status</Th>
            <Th>Attempt</Th>
            <Th>HTTP Status</Th>
            <Th>Error</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {logs.map((log) => (
            <Tr key={`${log.webhook_id}-${log.attempt_number}`}>
              <Td>
                <Code>{log.webhook_id}</Code>
              </Td>
              <Td>{new Date(log.timestamp).toLocaleString()}</Td>
              <Td>
                <Badge colorScheme={getStatusColor(log.status)}>
                  {log.status}
                </Badge>
              </Td>
              <Td>{log.attempt_number}</Td>
              <Td>{log.http_status || '-'}</Td>
              <Td>{log.error_message || '-'}</Td>
              <Td>
                <Button
                  size="sm"
                  colorScheme="blue"
                  onClick={() => showPayload(log.payload)}
                >
                  View Payload
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>

      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Webhook Payload</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <Code display="block" whiteSpace="pre" p={4}>
              {JSON.stringify(selectedPayload, null, 2)}
            </Code>
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  );
}

export default WebhookLogs;