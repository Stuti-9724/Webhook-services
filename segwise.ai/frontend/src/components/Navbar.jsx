import { Box, Flex, Button, Heading } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';

function Navbar() {
  return (
    <Box bg="blue.500" px={4} py={3}>
      <Flex maxW="container.xl" mx="auto" justify="space-between" align="center">
        <Heading as={RouterLink} to="/" size="lg" color="white">
          Webhook Service
        </Heading>
        <Button
          as={RouterLink}
          to="/subscriptions/new"
          colorScheme="whiteAlpha"
          variant="solid"
        >
          New Subscription
        </Button>
      </Flex>
    </Box>
  );
}

export default Navbar;