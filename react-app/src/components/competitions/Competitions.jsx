import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Text,
  VStack,
  useColorModeValue,
  Container,
} from '@chakra-ui/react';
import axios from 'axios';

const Competitions = () => {
  const [competitions, setCompetitions] = useState([]);
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  useEffect(() => {
    const fetchCompetitions = async () => {
      try {
        const response = await axios.get(`http://localhost:8001/api/competitions`);
        setCompetitions(response.data);
      } catch (error) {
        console.error('Error fetching competitions:', error);
      }
    };

    fetchCompetitions();
  }, []);

  return (
    <Container maxW="container.xl" py={5}>
      <VStack spacing={5} align="stretch">
        <Heading size="lg" mb={4}>
          Competitions ({competitions.length})
        </Heading>
        <Box
          bg={bgColor}
          shadow="md"
          borderRadius="lg"
          borderWidth="1px"
          borderColor={borderColor}
          overflow="hidden"
        >
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Name</Th>
                <Th>Area</Th>
              </Tr>
            </Thead>
            <Tbody>
              {competitions.map((competition) => (
                <Tr key={competition.id}>
                  <Td>
                    <Text fontWeight="medium">{competition.name}</Text>
                  </Td>
                  <Td>{competition.area}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>
      </VStack>
    </Container>
  );
};

export default Competitions;

