import * as ActionTypes from '../actions/actionTypes';

const INITIAL_STATE = {
  topics: [],
};

export const Topics = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case ActionTypes.ADD_TOPIC: {
      if (state.topics.includes(action.payload)) return state;
      else return { ...state, topics: state.topics.concat(action.payload) };
    }
    default:
      return state;
  }
};
