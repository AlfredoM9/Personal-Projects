import React, {Component} from 'react';
import Ninjas from "./Ninjas";
import AddNinja from './AddNinja'

class App extends Component {
    state = {
        ninjas: [{name:"Alfredo", age:25, belt:"white", id: 1},
                 {name:"Lucy", age:12, belt:"black", id:2},
                 {name:"Edrei", age:9, belt: "black", id:3}]
    };

    addNinja =(newNinja) => {
        newNinja.id = Math.random();
        let ninjas = [...this.state.ninjas, newNinja];
        this.setState({
            ninjas: ninjas
        })
    }

    deleteNinja =(id) => {
        let ninjas = this.state.ninjas.filter(ninja => {
            return ninja.id !== id
        });

        this.setState({
            ninjas: ninjas
        });
    }

    //Beginning of Component and automatically starts when created
    componentDidMount() {
        console.log('component mounted');
    }

    //Automatically starts when component is changed or updated
    componentDidUpdate(prevProps, prevState, snapshot) {
        console.log('component updated');
        console.log(prevProps, prevState);
    }

    render() {
        return (
            <div className="App">
                <h1>My First React App!</h1>
                <p>Welcome :)</p>

                <Ninjas ninjas={this.state.ninjas} deleteNinja={this.deleteNinja}/>
                <AddNinja addNinjaProp={this.addNinja}/>
            </div>
        );
    }
}

export default App;
