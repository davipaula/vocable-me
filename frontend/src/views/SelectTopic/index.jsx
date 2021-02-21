import React from 'react';

// i18n
import i18n from '../../i18n/index';
import { useTranslation } from 'react-i18next';

// Constants
import { topics } from './topics';

// Styles
import './styles.css';

export default function SelectTopic() {
  const { t } = useTranslation();
  return (
    <main className="topics-scene">
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
