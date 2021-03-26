import * as ActionTypes from '../actions/actionTypes';

const INITIAL_STATE = {
  topics: [],
};

export const Topics = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case ActionTypes.ADD_REMOVE_TOPIC: {
      if (state.topics.includes(action.payload)) {
        const topics = [...state.topics];
        topics.map((topic, index) => {
          topic === action.payload && topics.splice(index, 1);
        });
        return { ...state, topics: topics };
      } else {
        return { ...state, topics: state.topics.concat(action.payload) };
      }
    }
    default:
      return state;
  }
};
