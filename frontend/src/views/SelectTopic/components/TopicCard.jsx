import React from 'react';
import '../styles.css';

export default function TopicCard(props) {
  const { index, topic, comingSoon, onClick, selected } = props;
  return (
    <div
      key={index}
      className={`${comingSoon ? 'tooltip' : 'enabled-topics'}`}
      onClick={() => onClick && !comingSoon && onClick(topic.label)}
    >
      <h3
        className={`${comingSoon ? 'disabled-topics' : 'enabled-topics'} ${
          selected ? 'chosen-topic' : ''
        }`}
      >
        {' '}
        {topic.icon}
        {topic.label}
      </h3>
      {comingSoon && (
        <span className="tooltiptext">This topic is coming soon!</span>
      )}
    </div>
  );
}
