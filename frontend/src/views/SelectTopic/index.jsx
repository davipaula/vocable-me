import React, { Component } from 'react';

// i18n
import i18n from '../../i18n/index';
import { useTranslation } from 'react-i18next';

// Constants
import { topics } from './topics';

// Styles
import './styles.css';

export default class SelectTopic extends Component {
  componentDidMount() {
    fetch('http://localhost:8000/api/v1/topics/').then((res) =>
      console.log(res.json())
    );
  }

  render() {
    // const { t } = useTranslation();
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
        <div className="topics-container">
          {topics.map((topic, index) => {
            return (
              <div key="index">
                <h3>
                  {' '}
                  {topic.icon}
                  {topic.label}
                </h3>
              </div>
            );
          })}
        </div>
      </main>
    );
  }
}
