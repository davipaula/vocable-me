import React from 'react';

// Icons
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faUtensils,
  faUserTie,
  faLaptopCode,
  faFilm,
  faGuitar,
  faHandshake,
  faDumbbell,
  faBook,
  faBalanceScale,
  faPalette,
  faTv,
  faFlask,
  faGlobeAmericas,
  faHeart,
} from '@fortawesome/free-solid-svg-icons';

// i18n
import i18n from '../../i18n/index';

export const actualTopics = (topics) => {
  let topicsWithIcons = [];
  topics.map((topic, index) => {
    switch (topic) {
      case 'technology':
        return topicsWithIcons.push({
          label: topic,
          icon: <FontAwesomeIcon icon={faLaptopCode} />,
        });
      case 'entertainment':
        return topicsWithIcons.push({
          label: topic,
          icon: <FontAwesomeIcon icon={faTv} />,
        });
      case 'design':
        return topicsWithIcons.push({
          label: topic,
          icon: <FontAwesomeIcon icon={faPalette} />,
        });
      case 'business':
        return topicsWithIcons.push({
          label: topic,
          icon: <FontAwesomeIcon icon={faUserTie} />,
        });
      case 'science':
        return topicsWithIcons.push({
          label: topic,
          icon: <FontAwesomeIcon icon={faFlask} />,
        });
      case 'global issues':
        return topicsWithIcons.push({
          label: topic,
          icon: <FontAwesomeIcon icon={faGlobeAmericas} />,
        });
      default:
        return topicsWithIcons.push({
          label: topic,
          icon: <FontAwesomeIcon icon={faHeart} />,
        });
    }
  });
  return topicsWithIcons;
};

export const comingSoonTopics = [
  {
    label: i18n.t('topics.culinary'),
    icon: <FontAwesomeIcon icon={faUtensils} />,
  },
  {
    label: i18n.t('topics.movies'),
    icon: <FontAwesomeIcon icon={faFilm} />,
  },
  {
    label: i18n.t('topics.music'),
    icon: <FontAwesomeIcon icon={faGuitar} />,
  },
  {
    label: i18n.t('topics.politics'),
    icon: <FontAwesomeIcon icon={faHandshake} />,
  },
  {
    label: i18n.t('topics.sports'),
    icon: <FontAwesomeIcon icon={faDumbbell} />,
  },
  {
    label: i18n.t('topics.literature'),
    icon: <FontAwesomeIcon icon={faBook} />,
  },
  // {
  //   label: i18n.t('topics.law'),
  //   icon: <FontAwesomeIcon icon={faBalanceScale} />,
  // },
];
