import React from 'react';
import logo from './logo.svg';
import './App.css';
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import {ApolloProvider} from 'react-apollo';
import ApolloClient from "apollo-boost";
import gql from 'graphql-tag';



// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();


const client = new ApolloClient({
	uri: 'http://algorithmetic.herokuapp.com/v1alpha1/graphql'
	});

client
  .query({
    query: gql`
    {
		stat {
			tags
			cate
			totalcate
		}
		transfer {
			problem
			aid
		}
	}
    `
  })
  .then(result => console.log(result));
  
// check console logs for Hasura output Kevin
// just a sample of what could be done with Hasura for this app (pulling current question to a webpage, pulling current stats of the user to the webpage
// the best thing would probably be to do with this would be to set up a subscription service that continuously pulls from the GraphQL interface (we did this in the GraphIQL ide on Heroku as a proof of concept)
// mutations could also be used instead of the php nonsense we did

function App() {
  return null;
}
ReactDOM.render(<App />, document.getElementById('root'));
export default App;
