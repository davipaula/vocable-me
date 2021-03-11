import * as ActionTypes from './actionTypes';

export const addTopic = (topic) => (dispatch) => {
  dispatch({
    type: ActionTypes.ADD_TOPIC,
    payload: topic,
  });
};
