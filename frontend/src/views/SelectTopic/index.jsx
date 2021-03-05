import React, { Component } from 'react';

// i18n
import i18n from '../../i18n/index';

// Constants
import { comingSoonTopics, actualTopics } from './topics';

// Components
import Loader from 'react-loader-spinner';

// Styles
import './styles.css';

export default class SelectTopic extends Component {
  state = {
    topics: [],
    loading: false,
  };
  componentDidMount() {
    this.setState({ loading: true });
    fetch('http://localhost:8000/api/v1/topics/')
      .then((res) => res.json())
      .then((data) => this.setState({ loading: false, topics: data.topics }))
      .catch((err) => {
        console.error(err);
        this.setState({ loading: false });
      });
  }

  render() {
    // const { t } = useTranslation();
    const { topics, loading } = this.state;
    const availableTopics = topics.length > 0 && actualTopics(topics);

    return (
      <main className="topics-scene">
        <div className="logo-container">
          <img
            src="/assets/logo_transparent.png"
            alt="site logo"
            className="site-logo"
          />
        </div>
        <h1 className="topics-title">{i18n.t('topics.title')}</h1>
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
            {availableTopics &&
              availableTopics.map((topic, index) => {
                return (
                  <div key={index} className="enabled-topics">
                    <h3 className="enabled-topics">
                      {' '}
                      {topic.icon}
                      {topic.label}
                    </h3>
                  </div>
                );
              })}
            {comingSoonTopics.map((topic, index) => {
              return (
                <div key={index} className="tooltip">
                  <h3 className="disabled-topics">
                    {' '}
                    {topic.icon}
                    {topic.label}
                  </h3>
                  <span className="tooltiptext">
                    This topic is coming soon!
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </main>
    );
  }
}
