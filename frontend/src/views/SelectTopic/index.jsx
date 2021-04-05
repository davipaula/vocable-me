import React, { Component } from 'react';
import { connect } from 'react-redux';

// Constants
import { comingSoonTopics, actualTopics } from './topics';

// Components
import Loader from 'react-loader-spinner';
import TopicCard from './components/TopicCard';
import CTA from './components/CTA';

// Actions
import { addRemoveTopic, toggleModal } from '../../redux/actions/actionTopics';

// Styles
import './styles.css';

const mapStateToProps = (state) => {
  return {
    selectedTopics: state.topics,
  };
};

const mapDispatchToProps = (dispatch) => ({
  addRemoveTopic: (topic) => {
    dispatch(addRemoveTopic(topic));
  },
  toggleModal: (open) => {
    dispatch(toggleModal(open));
  },
});

class SelectTopic extends Component {
  state = {
    availableTopics: [],
    loading: false,
  };
  componentDidMount() {
    this.setState({ loading: true });
    fetch('http://localhost/api/v1/topics/')
      .then((res) => res.json())
      .then((data) =>
        this.setState({ loading: false, availableTopics: data.topics })
      )
      .catch((err) => {
        console.error(err);
        this.setState({ loading: false });
      });
  }

  render() {
    // const { t } = useTranslation();
    const { availableTopics, loading } = this.state;
    const { addRemoveTopic, selectedTopics, toggleModal } = this.props;
    const topicsWithIcons =
      availableTopics.length > 0 && actualTopics(availableTopics);

    return (
      <main className="topics-scene">
        <div className="logo-container">
          <img
            src="/assets/logo_transparent.png"
            alt="site logo"
            className="site-logo"
          />
        </div>
        <CTA selectedTopics={selectedTopics} toggleModal={toggleModal} />
        {loading ? (
          <Loader
            type="Circles"
            width={300}
            height={300}
            color="#008080"
            className="loader"
          />
        ) : (
          <div className="topics-container">
            {topicsWithIcons &&
              topicsWithIcons.map((topic, index) => {
                const selectedTopic = selectedTopics.topics.includes(
                  topic.label
                );
                return (
                  <TopicCard
                    topic={topic}
                    comingSoon={false}
                    index={index}
                    onClick={addRemoveTopic}
                    selected={selectedTopic}
                    key={`${topic}-${index}`}
                  />
                );
              })}
            {comingSoonTopics.map((topic, index) => {
              return (
                <TopicCard
                  topic={topic}
                  comingSoon={true}
                  index={index}
                  onClick={addRemoveTopic}
                  key={`${topic}-${index}`}
                />
              );
            })}
          </div>
        )}
      </main>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(SelectTopic);
