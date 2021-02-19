import React from 'react';

// i18n
import i18n from '../../i18n/index';
import { useTranslation } from 'react-i18next';

// Constants
import { topics } from './topics';

export default function SelectTopic() {
  const { t } = useTranslation();
  return (
    <main>
      <h1>{i18n.t('topics.title')}</h1>
      <div className="topics-container">
        {topics.map((topic, index) => {
          return (
            <div key="index">
              {topic.icon}
              {topic.label}
            </div>
          );
        })}
      </div>
    </main>
  );
}
