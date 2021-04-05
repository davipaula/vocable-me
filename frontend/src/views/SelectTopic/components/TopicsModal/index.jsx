import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

// Components
import Modal from '@material-ui/core/Modal';
import Backdrop from '@material-ui/core/Backdrop';
import Fade from '@material-ui/core/Fade';

// Actions
import {
  toggleModal,
  editWordsNr,
} from '../../../../redux/actions/actionTopics';

// Styles
import './modalStyles.css';

const mapStateToProps = (state) => {
  return {
    selectedTopics: state.topics,
    modalOpen: state.topics.modalOpen,
    wordsNr: state.topics.wordsNr,
  };
};

const mapDispatchToProps = (dispatch) => ({
  toggleModal: (open) => {
    dispatch(toggleModal(open));
  },
  editWordsNr: (number) => {
    dispatch(editWordsNr(number));
  },
});

class TopicsModal extends Component {
  handleClose = () => {
    this.props.toggleModal(false);
  };

  render() {
    const { modalOpen, editWordsNr, wordsNr } = this.props;
    if (modalOpen === false) return null;
    return (
      <Modal
        aria-labelledby="topics-modal-title"
        aria-describedby="topics-modal-description"
        className="topics-modal"
        open={modalOpen}
        onClose={this.handleClose}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
        }}
      >
        <Fade in={modalOpen}>
          <div className="modal-content">
            <h2 id="topics-modal-title">Let's start!</h2>
            <div id="topics-modal-description">
              How many new words per topic would you like to learn today?
              <select
                value={wordsNr}
                onChange={(e) => editWordsNr(e.target.value)}
              >
                <option value={5}>5</option>
                <option value={10}>10</option>
                <option value={15}>15</option>
              </select>
              <Link to="/sentences">
                <button className="submit-modal">NEXT</button>
              </Link>
            </div>
          </div>
        </Fade>
      </Modal>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(TopicsModal);
