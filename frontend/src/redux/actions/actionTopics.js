import * as ActionTypes from './actionTypes';

export const addRemoveTopic = (topic) => (dispatch) => {
  dispatch({
    type: ActionTypes.ADD_REMOVE_TOPIC,
    payload: topic,
  });
};
