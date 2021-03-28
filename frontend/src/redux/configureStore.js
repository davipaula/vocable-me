import { compose } from 'redux';
import { configureStore } from '@reduxjs/toolkit';
import { Topics } from './reducers/Topics';

export const ConfigureStore = () => {
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

  const rootReducer = (state = null, action) => {
    return {
      ...(state && { topics: Topics(state.topics, action) }),
    };
  };
  // TODO: When deploying, check .env to remove logger
  return configureStore(
    {
      reducer: {
        topics: Topics,
      },
    },
    // logger must be the last middleware of the chain
    // composeEnhancers(applyMiddleware(reduxThunk, logger))
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
  );
};

export const store = ConfigureStore();
