import { createStore, applyMiddleware, compose } from 'redux';
import reduxThunk from 'redux-thunk';
import { Topics } from './reducers/Topics';
import * as ActionTypes from './actions/actionTypes';

// Redux LOGGER
// const logger = createLogger({
//   predicate: (getState, action) => {
//     var condition = true;
//     condition &= !action.type.includes(ActionTypes.ROUTE_CHANGED); // Filter the ROUTE_CHANGED Action, to avoid logging it in the console.
//     return condition;
//   },
// });

export const ConfigureStore = () => {
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

  const rootReducer = (state = null, action) => {
    return {
      ...(state && { topics: Topics(state.topics, action) }),
    };
  };
  // TODO: When deploying, check .env to remove logger
  return createStore(
    rootReducer,
    // logger must be the last middleware of the chain
    // composeEnhancers(applyMiddleware(reduxThunk, logger))
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
  );
};

export const store = ConfigureStore();
