import * as ActionTypes from './actionTypes';

export const addRemoveTopic = (topic) => (dispatch) => {
  dispatch({
    type: ActionTypes.ADD_REMOVE_TOPIC,
    payload: topic,
  });
};

export const toggleModal = (open) => (dispatch) => {
  dispatch({
    type: ActionTypes.TOGGLE_MODAL,
    payload: open,
  });
};

export const editWordsNr = (number) => (dispatch) => {
  dispatch({
    type: ActionTypes.WORDS_NR,
    payload: number,
  });
};
