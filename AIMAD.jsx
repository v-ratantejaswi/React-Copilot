import {
  ChakraProvider,
  Box,
  Button,
  Flex,
  FormControl,
  FormLabel,
  Heading,
  IconButton,
  Input,
  SimpleGrid,
  Text,
  useToast,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { RiSendPlaneFill } from "react-icons/ri";
import { BiSearch, BiDotsVerticalRounded } from "react-icons/bi";
import { MdFlight, MdRefresh } from "react-icons/md";
import { FaUserEdit } from "react-icons/fa";

const AIMAD = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [customerDetails, setCustomerDetails] = useState({});
  const toast = useToast();

  useEffect(() => {
    fetch("/api/customer-details")
      .then((res) => res.json())
      .then((data) => setCustomerDetails(data));
  }, []);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim() === "") {
      toast({
        title: "Message is empty",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    const newMessageObj = {
      sender: "agent",
      message: newMessage,
    };
    setMessages([...messages, newMessageObj]);
    setNewMessage("");
  };

  return (
    <ChakraProvider>
      <Box as="header" bg="blue.500" py={3}>
        <Heading textAlign="center" color="white" size="lg">AI Assistant Dashboard</Heading>
        <Text textAlign="center" color="white" mt={2}>Enhance your customer support with AI</Text>
      </Box>
      <Tabs variant="enclosed" colorScheme="blue" isFitted>
        <TabList>
          <Tab>Chat</Tab>
          <Tab>Customer Details</Tab>
          <Tab>Flight Actions</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <Flex direction="column" h="80vh">
              <Box flex="1" overflowY="auto">
                {messages.map((message, index) => (
                  <Flex
                    key={index}
                    justifyContent={message.sender === "agent" ? "flex-end" : "flex-start"}
                    alignItems="center"
                    w="100%"
                  >
                    <Box
                      p={2}
                      borderRadius="md"
                      bg={message.sender === "agent" ? "blue.100" : "gray.100"}
                      color={message.sender === "agent" ? "blue.600" : "gray.600"}
                      maxWidth="75%"
                    >
                      <Text>{message.message}</Text>
                    </Box>
                  </Flex>
                ))}
              </Box>
              <form onSubmit={handleSendMessage}>
                <Flex h="64px" alignItems="center">
                  <Input
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Type your message here"
                    w="calc(100% - 104px)"
                  />
                  <IconButton
                    type="submit"
                    aria-label="Send"
                    icon={<RiSendPlaneFill />}
                    colorScheme="blue"
                    ml={4}
                  />
                  <IconButton
                    aria-label="Search"
                    icon={<BiSearch />}
                    colorScheme="gray"
                    ml={4}
                  />
                  <IconButton
                    aria-label="More"
                    icon={<BiDotsVerticalRounded />}
                    colorScheme="gray"
                    ml={4}
                  />
                </Flex>
              </form>
            </Flex>
          </TabPanel>
          <TabPanel>
            <SimpleGrid columns={2} spacing={4}>
              <FormControl isReadOnly>
                <FormLabel>Name</FormLabel>
                <Input value={customerDetails.name || ""} />
              </FormControl>
              <FormControl isReadOnly>
                <FormLabel>Email</FormLabel>
                <Input value={customerDetails.email || ""} />
              </FormControl>
              <FormControl isReadOnly>
                <FormLabel>Phone</FormLabel>
                <Input value={customerDetails.phone || ""} />
              </FormControl>
            </SimpleGrid>
          </TabPanel>
          <TabPanel>
            <SimpleGrid columns={1} spacing={4}>
              <Button
                leftIcon={<MdFlight />}
                colorScheme="green"
                onClick={() => toast({ title: "Check Flight Status", status: "info" })}
              >
                Check Flight
              </Button>
              <Button
                leftIcon={<FaUserEdit />}
                colorScheme="blue"
                onClick={() => toast({ title: "Update Customer Info", status: "info" })}
              >
                Update Info
              </Button>
              <Button
                leftIcon={<MdRefresh />}
                colorScheme="teal"
                onClick={() => toast({ title: "Refresh Data", status: "info" })}
              >
                Refresh Data
              </Button>
            </SimpleGrid>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </ChakraProvider>
  );
};

export default AIMAD;