import React, {useState} from 'react';
import { StyleSheet, Text, View, Button, TextInput, ScrollView, FlatList, TouchableOpacity, Alert, TouchableWithoutFeedback, Keyboard } from 'react-native';
import Header from "./components/header";
import TodoItem from "./components/todoItem";
import AddTodo from "./components/addTodo";
import SandBox from "./components/sandBox";


export default function App() {
  const [name, setName] = useState('Alfredo'); // Video 4 & 5
  const [age, setAge] = useState('19'); // Video 5
  const [person, setPerson] = useState({name: 'Mario', age:40}); // Video 4
  // Video 6 & 7
  const [people, setPeople] = useState([
    {name: 'Alfredo', id: '1'},
    {name: 'Edrei', id: '2'},
    {name: 'Lucy', id: '3'},
    {name: 'Martha', id:'4'},
    {name: 'Karina', id: '5'},
    {name: 'Rafa', id: '6'},
    {name: 'AlfredoT', id: '7'}
  ]);

  //Video 9-15 Todo App
  const [todos, setTodos] = useState([
    {text: 'buy coffee', key: '1'},
    {text: 'create an app', key: '2'},
    {text: 'play on the switch', key: '3'}
  ]);
  //Inheritance for styles doesn't necessary work for all in JSX
  //One exception is text child component inherits the parent text style

  /*
  /*******Part of video 3***************
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.boldText}>Hello World</Text>
      </View>
      <View style={styles.body}>
        <Text>Lorem ipsum dolor sit amet</Text>
        <Text>Lorem ipsum dolor sit amet</Text>
        <Text>Lorem ipsum dolor sit amet</Text>
        <Text>Lorem ipsum dolor sit amet</Text>
      </View>
    </View>
  );

  /***********Part of video 4*****************************
  const clickHandler = () => {
    setName('Edrei');
    setPerson({name: 'Luigi', age: 45});
  }
  return(
    <View style={styles.container}>
      <Text>My name is {name}</Text>
      <Text>His name is {person.name} and his age is {person.age}</Text>
      <View style={styles.buttonContainer}>
        <Button title='update name' onPress={clickHandler}/>
      </View>

   /******************Part of video 5****************************************
      <Text>Enter name:</Text>
      <TextInput
          multiline
          style={styles.input}
          placeholder='e.g. John Doe'
          onChangeText={(val) => setName(val)}/>
      <Text>Enter age:</Text>
      <TextInput
          keyboardType='numeric'
          style={styles.input}
          placeholder='e.g. 30'
          onChangeText={(val) => setAge(val)}/>
       <Text>My name is {name} and my age is {age}</Text>

    </View>
  );
   */
  /***********************************Video 6*********************
  return (
      <View style={styles.container}>
        <ScrollView>
          {people.map(person => (
              <View key={person.key}>
                <Text style={styles.item}>{person.name}</Text>
              </View>
            )
          )}
        </ScrollView>
      </View>
  )
   */

  /*****************************Video 7 & 8********************
  const pressHandler = (id) => {
    console.log(id);
    setPeople((previousPeople) => {
      return previousPeople.filter(person => person.id != id)
    });
  }
  return (
      <View style={styles.container}>
        <FlatList
          numColumns ={2}
          keyExtractor={(item) => item.id}
          data={people}
          renderItem={({item}) => (
              <TouchableOpacity onPress={() => pressHandler(item.id)}>
                <Text style={styles.item}>{item.name}</Text>
              </TouchableOpacity>
          )}
        />
      </View>
  )
   */

  //********************Video 9-15 Todo App
  const pressHandler = (key) => {
    setTodos((previousTodos) => {
      return previousTodos.filter(todo => todo.key != key);
    })
  }

  const submitHandler = (text) => {

    if(text.length > 3)
    {
      setTodos ((previousTodos) => {
        return [
          {text: text, key: Math.random().toString()},
          ...previousTodos
        ]
      })
      Keyboard.dismiss();
    }

    else
    {
      Alert.alert('Oops!', 'Todos must be over three chars long', [
        {text: 'Understood', onPress: () => console.log('alert closed')}
      ])
    }

  }
  return(
      //<SandBox />
      <TouchableWithoutFeedback onPress={() => {
        Keyboard.dismiss();
        console.log('dismissed keyboard');
      }}>
        <View style={styles.container}>
          {/* header */}
          <Header/>
          <View style={styles.content}>
            {/* to form */}
            <AddTodo submitHandler={submitHandler}/>
            <View style={styles.list}>
              <FlatList
                data={todos}
                renderItem={({item}) => (
                    <TodoItem item={item} pressHandler={pressHandler}/>
                )}
              />
            </View>
          </View>
        </View>
      </TouchableWithoutFeedback>
  )
}

const styles = StyleSheet.create({
  /*****************Video 3-5
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  header: {
    backgroundColor: 'pink',
    padding: 20,
  },
  boldText: {
    fontWeight: 'bold'
  },
  body: {
    backgroundColor: 'yellow',
    padding: 20
  },
  buttonContainer: {
    marginTop: 20
  },
  input: {
    borderWidth: 1,
    borderColor: '#777',
    padding: 8,
    margin: 10,
    width: 200,
  }

   */
  /*******************Video 6-8*******************
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingTop: 40,
    paddingHorizontal: 20
  },
  item: {
    marginTop: 24,
    padding: 30,
    backgroundColor: 'pink',
    fontSize: 24,
    marginHorizontal: 10,
  }
   */
  //******************Video 9-15 Todo App
  container: {
    flex: 1,
    backgroundColor: '#fff'
  },
  content: {
    padding: 40,
    flex: 1
  },
  list: {
    flex: 1,
    margin: 20,

  }
});
