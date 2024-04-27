#Importing necessary Libraries.
import openai
from flask import Flask, render_template, request, send_file, jsonify
import os

app = Flask(__name__)




OPENAI_API_KEY = os.getenv('OPENAI_API_KEY_RECS')
openai.api_key = OPENAI_API_KEY
design_doc_content = ""

"""
The generate method first takes in a prompt along with business type, and sends it to gpt4 to generate a design document markdown.
Then, that document, along with the code of the selected template and the business type is sent as a second prompt to gpt4 to
generate a .jsx file.
"""

def generate_design_doc(biz_type):
    print("Started Generating Design Document")
    # Placeholder prompt
    prompt_design_doc = f"""You are a UI/UX expert working with clients on a project. The end user wants to design an AI Assistant/Bot to work along with a {biz_type} Customer Service Agent. 
    The application is intended to help the agent by providing real-time information and guidance, enhancing the efficiency and effectiveness of customer support. 

    Provide the project design document with the following components. 
    -------------------------------
    Project Overview:
    Cover the high level objective of the assistant and focus on the goals of this application. This component defines the structure and organization of information within the product.

    Design Overview:
    List the components of the Application and give a detailed explanation of each component/page and its functionality.

    For each page, define 4 primary functionalities that are relevant to the use-case.

    Examples:

    Bank

    1) Show Account Details
    2) Edit Customer Details
    3) Perform Transactions
    4) Card Actions

    Travel Agency

    1) Manage Reservations
    2) Make Reservations
    3) Browse Packages
    4) Manage User Details

    Airline

    1) Manage Reservations
    2) Cancel and Rebook Flight
    3) Manage User Details
    4) Track Baggage and Complaints

    The first page must be the landing page. The 4 functionalities of the landing page must be linked in the page.
    Flow:
    Describe the behavior and interactions of the product's user interface. Include navigation flows, site maps. Also finalize a color palette and UX philosophy to follow.

    The implementation would be in React. Design accordingly.
    """
    completion = openai.chat.completions.create(
      model="gpt-4-turbo-2024-04-09",
      messages= [
        {
          "role": "system", "content":"You are a UI/UX expert consulting clients for a project. Generate a design document for the client strictly in the mentioned format."},
          {
            "role": "user", "content": prompt_design_doc

          }
        ],
        max_tokens=4096,
        temperature=0.0
    )
    doc = completion.choices[0].message.content

      
    with open("design_doc.md", "w", encoding='utf-8') as text_file:
      text_file.write(doc)
      print("Generated Design Document successfully\n")

    return doc


def generate_react_code(biz_type, template, text):
  print("Started Generating React Code")
  base_template_1 = """import {
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
  } from "@chakra-ui/react";
  import { useEffect, useState } from "react";
  import { AiOutlineSend } from "react-icons/ai";
  import { FaUserEdit } from "react-icons/fa";
  import { MdPayment, MdRefresh } from "react-icons/md";
  import { RiSendPlaneFill } from "react-icons/ri";
  import { BiSearch, BiDotsVerticalRounded } from "react-icons/bi";

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
          <Heading textAlign="center" color="white" size="lg">Customer Service Dashboard</Heading>
          <Text textAlign="center" color="white" mt={2}>Manage interactions and customer details</Text>
        </Box>
        <Flex h="100vh" w="100vw">
          <Box w="50vw" bg="gray.100" p={4}>
            <Heading size="md">Customer Details</Heading>
            <SimpleGrid columns={2} spacing={4} mt={4}>
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
            <Heading size="md" mt={6}>Actions</Heading>
            <SimpleGrid columns={3} spacing={4} mt={4}>
              <Button
                leftIcon={<MdPayment />}
                colorScheme="green"
                onClick={() => toast({ title: "Initiate Payment", status: "info" })}
              >
                Issue Refund
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
          </Box>
          <Box w="50vw" bg="white" p={4}>
            <Heading size="md">Chat</Heading>
            <Flex h="calc(100vh - 88px)" flexDir="column">
              <Box h="calc(100vh - 88px - 64px)" overflowY="auto">
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
          </Box>
        </Flex>
      </ChakraProvider>
    );
  };

  export default AIMAD;

  """

  base_template_2 = """import {
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
    Drawer,
    DrawerBody,
    DrawerFooter,
    DrawerHeader,
    DrawerOverlay,
    DrawerContent,
    useDisclosure,
  } from "@chakra-ui/react";
  import { useEffect, useState } from "react";
  import { RiSendPlaneFill } from "react-icons/ri";
  import { BiSearch, BiDotsVerticalRounded } from "react-icons/bi";
  import { MdPayment, MdRefresh } from "react-icons/md";
  import { FaUserEdit } from "react-icons/fa";

  const AIMAD = () => {
    const { isOpen, onOpen, onClose } = useDisclosure();
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
          <Heading textAlign="center" color="white" size="lg">Customer Service Dashboard</Heading>
          <Text textAlign="center" color="white" mt={2}>Manage interactions and customer details</Text>
        </Box>
        <Flex h="100vh">
          <Box flex="1" bg="white" p={4}>
            <Heading size="md">Chat</Heading>
            <Flex h="calc(100vh - 88px)" flexDir="column">
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
          </Box>
          <Box width="400px" bg="gray.100" p={4}>
            <Button onClick={onOpen} colorScheme="blue" w="100%">Open Details and Actions</Button>
          </Box>
          <Drawer placement="right" onClose={onClose} isOpen={isOpen} size="md">
            <DrawerOverlay />
            <DrawerContent>
              <DrawerHeader borderBottomWidth="1px">Customer Details and Actions</DrawerHeader>
              <DrawerBody>
                <SimpleGrid columns={1} spacing={4}>
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
                <Heading size="md" mt={6}>Actions</Heading>
                <SimpleGrid columns={1} spacing={4}>
                  <Button
                    leftIcon={<MdPayment />}
                    colorScheme="green"
                    onClick={() => toast({ title: "Initiate Payment", status: "info" })}
                  >
                    Issue Refund
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
              </DrawerBody>
              <DrawerFooter>
                <Button variant="outline" mr={3} onClick={onClose}>
                  Close
                </Button>
              </DrawerFooter>
            </DrawerContent>
          </Drawer>
        </Flex>
      </ChakraProvider>
    );
  };

  export default AIMAD;

  """


  base_template_3 = """import {
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
  import { MdPayment, MdRefresh } from "react-icons/md";
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
          <Heading textAlign="center" color="white" size="lg">Customer Service Dashboard</Heading>
          <Text textAlign="center" color="white" mt={2}>Manage interactions and customer details</Text>
        </Box>
        <Tabs variant="enclosed" colorScheme="blue" isFitted>
          <TabList>
            <Tab>Chat</Tab>
            <Tab>Customer Details</Tab>
            <Tab>Actions</Tab>
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
                  leftIcon={<MdPayment />}
                  colorScheme="green"
                  onClick={() => toast({ title: "Initiate Payment", status: "info" })}
                >
                  Issue Refund
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

  """
  #Sends template based on selection.
  if template == "template1":
     base_template = base_template_1
  elif template == "template2":
     base_template = base_template_2
  else:
     base_template = base_template_3




  completion = openai.chat.completions.create(
      # model="gpt-4-turbo",
      model = "gpt-4-turbo-2024-04-09",
      messages= [
        {
          "role": "system", "content":"You are a React Developer. Generate a React code for the client strictly in the mentioned format."},
          {
            "role": "user", "content": f"""You are an expert React Developer. You are to design the User Interace (UI/UX) for an AI Assistant Application that aids and provides information to a customer support agent. Generate fully-functional code using React and Chakra-UI for this application. The user interface must have two primary colums: The right one will be a customer chat window where the support agent interacts with the customer. The left one consists of various functionalities specific to the {biz_type}. Use ONLY Chakra UI for the code. Minimize additional library installation. The purpose of the AI Assistant is to provide real-time information and guidance to agents, enhancing the efficiency and effectiveness of customer support.

  Use this code as the base template for generating code. Change only the required components.
  {base_template}
  Use the following guidelines when generating components. ONLY generate functionalities from the guidelines.  Change the required components, buttons, and functionalities. Replace any irrelevant components with the required components and buttons.
  {text}

  Generate COMPLETE, immediately runnable code. Only code. Nothing else. No explanations at all. Provide complete, immediately runnable code. The method name should be AIMAD
  """
          }
        ],
        max_tokens=4096,
        temperature=0.0
    )
  try:
      code = completion.choices[0].message.content
      code = '\n'.join(code.split('\n')[1:-1])
      with open("AIMAD.jsx", "w", encoding='utf-8') as text_file:
        text_file.write(code)
      print("Generated React code successfully\n")
  except:
      print(completion)
  return code







def generate(biz_type, template):
  print(biz_type,template)
  base_template_1 = """import {
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
  } from "@chakra-ui/react";
  import { useEffect, useState } from "react";
  import { AiOutlineSend } from "react-icons/ai";
  import { FaUserEdit } from "react-icons/fa";
  import { MdPayment, MdRefresh } from "react-icons/md";
  import { RiSendPlaneFill } from "react-icons/ri";
  import { BiSearch, BiDotsVerticalRounded } from "react-icons/bi";

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
          <Heading textAlign="center" color="white" size="lg">Customer Service Dashboard</Heading>
          <Text textAlign="center" color="white" mt={2}>Manage interactions and customer details</Text>
        </Box>
        <Flex h="100vh" w="100vw">
          <Box w="50vw" bg="gray.100" p={4}>
            <Heading size="md">Customer Details</Heading>
            <SimpleGrid columns={2} spacing={4} mt={4}>
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
            <Heading size="md" mt={6}>Actions</Heading>
            <SimpleGrid columns={3} spacing={4} mt={4}>
              <Button
                leftIcon={<MdPayment />}
                colorScheme="green"
                onClick={() => toast({ title: "Initiate Payment", status: "info" })}
              >
                Issue Refund
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
          </Box>
          <Box w="50vw" bg="white" p={4}>
            <Heading size="md">Chat</Heading>
            <Flex h="calc(100vh - 88px)" flexDir="column">
              <Box h="calc(100vh - 88px - 64px)" overflowY="auto">
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
          </Box>
        </Flex>
      </ChakraProvider>
    );
  };

  export default AIMAD;

  """

  base_template_2 = """import {
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
    Drawer,
    DrawerBody,
    DrawerFooter,
    DrawerHeader,
    DrawerOverlay,
    DrawerContent,
    useDisclosure,
  } from "@chakra-ui/react";
  import { useEffect, useState } from "react";
  import { RiSendPlaneFill } from "react-icons/ri";
  import { BiSearch, BiDotsVerticalRounded } from "react-icons/bi";
  import { MdPayment, MdRefresh } from "react-icons/md";
  import { FaUserEdit } from "react-icons/fa";

  const AIMAD = () => {
    const { isOpen, onOpen, onClose } = useDisclosure();
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
          <Heading textAlign="center" color="white" size="lg">Customer Service Dashboard</Heading>
          <Text textAlign="center" color="white" mt={2}>Manage interactions and customer details</Text>
        </Box>
        <Flex h="100vh">
          <Box flex="1" bg="white" p={4}>
            <Heading size="md">Chat</Heading>
            <Flex h="calc(100vh - 88px)" flexDir="column">
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
          </Box>
          <Box width="400px" bg="gray.100" p={4}>
            <Button onClick={onOpen} colorScheme="blue" w="100%">Open Details and Actions</Button>
          </Box>
          <Drawer placement="right" onClose={onClose} isOpen={isOpen} size="md">
            <DrawerOverlay />
            <DrawerContent>
              <DrawerHeader borderBottomWidth="1px">Customer Details and Actions</DrawerHeader>
              <DrawerBody>
                <SimpleGrid columns={1} spacing={4}>
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
                <Heading size="md" mt={6}>Actions</Heading>
                <SimpleGrid columns={1} spacing={4}>
                  <Button
                    leftIcon={<MdPayment />}
                    colorScheme="green"
                    onClick={() => toast({ title: "Initiate Payment", status: "info" })}
                  >
                    Issue Refund
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
              </DrawerBody>
              <DrawerFooter>
                <Button variant="outline" mr={3} onClick={onClose}>
                  Close
                </Button>
              </DrawerFooter>
            </DrawerContent>
          </Drawer>
        </Flex>
      </ChakraProvider>
    );
  };

  export default AIMAD;

  """


  base_template_3 = """import {
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
  import { MdPayment, MdRefresh } from "react-icons/md";
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
          <Heading textAlign="center" color="white" size="lg">Customer Service Dashboard</Heading>
          <Text textAlign="center" color="white" mt={2}>Manage interactions and customer details</Text>
        </Box>
        <Tabs variant="enclosed" colorScheme="blue" isFitted>
          <TabList>
            <Tab>Chat</Tab>
            <Tab>Customer Details</Tab>
            <Tab>Actions</Tab>
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
                  leftIcon={<MdPayment />}
                  colorScheme="green"
                  onClick={() => toast({ title: "Initiate Payment", status: "info" })}
                >
                  Issue Refund
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

  """
  #Sends template based on selection.
  if template == "template1":
     base_template = base_template_1
  elif template == "template2":
     base_template = base_template_2
  else:
     base_template = base_template_3
  

  OPENAI_API_KEY = os.getenv('OPENAI_API_KEY_RECS')

  openai.api_key = OPENAI_API_KEY


  def generate_design_doc(biz_type):
    prompt_design_doc = f"""You are a UI/UX expert working with clients on a project. The end user wants to design an AI Assistant/Bot to work along with a {biz_type} Customer Service Agent. 
  The application is intended to help the agent by providing real-time information and guidance, enhancing the efficiency and effectiveness of customer support. 

  Provide the project design document with the following components. 
  -------------------------------
  Project Overview:
  Cover the high level objective of the assistant and focus on the goals of this application. This component defines the structure and organization of information within the product.

  Design Overview:
  List the components of the Application and give a detailed explanation of each component/page and its functionality.

  For each page, define 4 primary functionalities that are relevant to the use-case.

  Examples:

  Bank

  1) Show Account Details
  2) Edit Customer Details
  3) Perform Transactions
  4) Card Actions

  Travel Agency

  1) Manage Reservations
  2) Make Reservations
  3) Browse Packages
  4) Manage User Details

  Airline

  1) Manage Reservations
  2) Cancel and Rebook Flight
  3) Manage User Details
  4) Track Baggage and Complaints

  The first page must be the landing page. The 4 functionalities of the landing page must be linked in the page.
  Flow:
  Describe the behavior and interactions of the product's user interface. Include navigation flows, site maps. Also finalize a color palette and UX philosophy to follow.

  The implementation would be in React. Design accordingly.
  """
    completion = openai.chat.completions.create(
      model="gpt-4-turbo-2024-04-09",
      messages= [
        {
          "role": "system", "content":"You are a UI/UX expert consulting clients for a project. Generate a design document for the client strictly in the mentioned format."},
          {
            "role": "user", "content": prompt_design_doc

          }
        ],
        max_tokens=4096,
        temperature=0.0
    )
    doc = completion.choices[0].message.content

      
    with open("design_doc.md", "w", encoding='utf-8') as text_file:
      text_file.write(doc)
    return doc

  def generate_react_code(text,biz_type):

    prompt_react = """
  You are an expert React Developer. You are to design the User Interace (UI/UX) for an AI Assistant Application that aids and provides information to a customer support agent. Generate fully-functional code using React and Chakra-UI for this application. The user interface must have two primary colums: The right one will be a customer chat window where the support agent interacts with the customer. The left one consists of various functionalities specific to the {biz_type}. Use ONLY Chakra UI for the code. Minimize additional library installation. The purpose of the AI Assistant is to provide real-time information and guidance to agents, enhancing the efficiency and effectiveness of customer support.

  Use this code as the base template for generating code. Change only the required components.
  {base_template}
  Use the following guidelines when generating components. ONLY generate functionalities from the guidelines.  Change the required components, buttons, and functionalities. Replace any irrelevant components with the required components and buttons. 
  {text}

  Generate only the Landing Page from the guidelines. Design the 4 functionalities strictly from the design document.

  Generate COMPLETE, immediately runnable code. Only code. Nothing else. No explanations at all. Provide complete, immediately runnable code. The method name should be AIMAD
  """.format(biz_type=biz_type, base_template=base_template, text=text)
    completion = openai.chat.completions.create(
      # model="gpt-4-turbo",
      model = "gpt-4-turbo-2024-04-09",
      messages= [
        {
          "role": "system", "content":"You are a React Developer. Generate a React code for the client strictly in the mentioned format."},
          {
            "role": "user", "content": f"""You are an expert React Developer. You are to design the User Interace (UI/UX) for an AI Assistant Application that aids and provides information to a customer support agent. Generate fully-functional code using React and Chakra-UI for this application. The user interface must have two primary colums: The right one will be a customer chat window where the support agent interacts with the customer. The left one consists of various functionalities specific to the {biz_type}. Use ONLY Chakra UI for the code. Minimize additional library installation. The purpose of the AI Assistant is to provide real-time information and guidance to agents, enhancing the efficiency and effectiveness of customer support.

  Use this code as the base template for generating code. Change only the required components.
  {base_template}
  Use the following guidelines when generating components. ONLY generate functionalities from the guidelines.  Change the required components, buttons, and functionalities. Replace any irrelevant components with the required components and buttons.
  {text}

  Generate COMPLETE, immediately runnable code. Only code. Nothing else. No explanations at all. Provide complete, immediately runnable code. The method name should be AIMAD
  """
          }
        ],
        max_tokens=4096,
        temperature=0.0
    )
    try:
        code = completion.choices[0].message.content
        code = '\n'.join(code.split('\n')[1:-1])
        with open("AIMAD.jsx", "w", encoding='utf-8') as text_file:
          text_file.write(code)
        # print(code)
    except:
        print(completion)


  des_doc_text = generate_design_doc(biz_type)
  print('Generated the design document')
  print('Now generating the React code...')




  generate_react_code(des_doc_text,biz_type)
  print('Generated the React code')



@app.route("/")
def home():
    
    return render_template("index.html")



@app.route("/submit", methods=["POST"])
def submit():
    business_type = request.form.get('biz_type')
    template = request.form.get('template')
    generate(business_type, template)
    return render_template("index.html",show_download=True)

@app.route("/generate_design", methods=["POST"])
def generate_design():
    biz_type = request.form.get('biz_type')
    template = request.form.get('template')
    design_doc_content = generate_design_doc(biz_type)
    if design_doc_content:
        return jsonify(status="partial", content=design_doc_content, message="Design document generated. Proceeding to React code...")

@app.route("/generate_react", methods=["POST"])
def generate_react():
    biz_type = request.form.get('biz_type')
    template = request.form.get('template')
    if generate_react_code(biz_type, template, design_doc_content):
        return jsonify(status="success", message="React code generated successfully")

@app.route("/about")
def about():
   return render_template("about.html")

    
@app.route("/download-js")
def download_js():
   path = "AIMAD.jsx"
   return send_file(path,as_attachment=True)


@app.route("/download-des")
def download_des():
   path = "design_doc.md"
   return send_file(path,as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)