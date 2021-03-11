import React, { Component } from 'react';
import { Routes } from './Routes';
import { store } from './redux/configureStore';
import { Provider } from 'react-redux';

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <Routes />
      </Provider>
    );
  }
}

export default App;
