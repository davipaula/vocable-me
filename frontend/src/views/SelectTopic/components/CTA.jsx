import React from 'react';
import i18n from '../../../i18n/index';
import TopicsModal from './TopicsModal/index';

export default function CTA(props) {
  const { selectedTopics, toggleModal } = props;

  return (
    <>
      <h2 className="topics-title">{i18n.t('topics.title')}</h2>
      <div className="cta-text ">
        <p>
          We're here to help expanding your vocabulary in your favorite topics.
          So please, let us know which stuff you're excited about by clicking on
          them, and, when you're ready for some action, click
          <button
            className={`${
              selectedTopics.topics && selectedTopics.topics.length < 1
                ? 'tooltip'
                : ''
            }`}
            onClick={() => {
              selectedTopics &&
                selectedTopics.topics.length > 0 &&
                toggleModal(true);
            }}
          >
            NEXT
            {selectedTopics.topics && selectedTopics.topics.length < 1 && (
              <span className="tooltiptext">
                Please, select at least 1 topic before moving on!
              </span>
            )}
          </button>
        </p>
      </div>
      <TopicsModal />
    </>
  );
}
