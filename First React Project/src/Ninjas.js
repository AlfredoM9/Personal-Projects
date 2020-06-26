import React from 'react'
import './Ninjas.css'
const Ninjas = ({ninjas, deleteNinja}) =>
{
        //console.log(this.props);
        //Props have to have same name as variables
        //const{name, age, belt} = this.props;
        const ninjaList = ninjas.map(ninja =>{
            //You can use the ternary operator as well
            //You can also just paste the code directly to the return template
            if(ninja.age > 18){
            return (
                <div className="ninja" key={ninja.id}>
                    <div>Name: {ninja.name}</div>
                    <div>Age: {ninja.age}</div>
                    <div>Belt: {ninja.belt}</div>
                    <button onClick={() => {deleteNinja(ninja.id)}}>Delete Ninja</button>
                </div>
            )}
            else
            {
                return null;
            }
        });
        return (
            <div className="ninja-list">
                {ninjaList}
            </div>
        )
}

export default Ninjas
