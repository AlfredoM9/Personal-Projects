import React from 'react';
import {createStackNavigator} from "@react-navigation/stack";
import {NavigationContainer} from "@react-navigation/native";
import Home from "../screens/home";
import ReviewDetails from "../screens/reviewDetails";
import Header from "../shared/header";

const Stack = createStackNavigator();

export default function homeNavigator({navigation}) {
    return (
        <Stack.Navigator initialRouteName='Home'
             screenOptions={{
                 headerStyle: {
                     backgroundColor: '#999',
                 },
                 headerTintColor: '#fff',
                 headerTitleStyle: {
                     fontWeight: 'bold',
                 },
             }}>
            <Stack.Screen name='Home' component={Home}
              options={{
                headerTitle: () => <Header navigation={navigation} title='GameZone'/>,
              }}
            />
            <Stack.Screen name='ReviewDetails' component={ReviewDetails}
                options={{
                    title: 'Review Details'
                }}
            />
        </Stack.Navigator>
    );
}
