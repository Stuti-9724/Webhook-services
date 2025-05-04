import { ChakraProvider, Container } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import SubscriptionList from './components/SubscriptionList';
import SubscriptionForm from './components/SubscriptionForm';
import WebhookLogs from './components/WebhookLogs';

function App() {
  return (
    <ChakraProvider>
      <Router>
        <Navbar />
        <Container maxW="container.xl" py={8}>
          <Routes>
            <Route path="/" element={<SubscriptionList />} />
            <Route path="/subscriptions/new" element={<SubscriptionForm />} />
            <Route path="/subscriptions/:id/logs" element={<WebhookLogs />} />
          </Routes>
        </Container>
      </Router>
    </ChakraProvider>
  );
}

export default App;