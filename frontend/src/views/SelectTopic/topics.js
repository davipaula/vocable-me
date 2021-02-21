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
} from '@fortawesome/free-solid-svg-icons';

// i18n
import i18n from '../../i18n/index';

export const topics = [
  {
    label: i18n.t('topics.culinary'),
    icon: <FontAwesomeIcon icon={faUtensils} />,
  },
  {
    label: i18n.t('topics.business'),
    icon: <FontAwesomeIcon icon={faUserTie} />,
  },
  {
    label: i18n.t('topics.technology'),
    icon: <FontAwesomeIcon icon={faLaptopCode} />,
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
  {
    label: i18n.t('topics.law'),
    icon: <FontAwesomeIcon icon={faBalanceScale} />,
  },
  {
    label: i18n.t('topics.design'),
    icon: <FontAwesomeIcon icon={faPalette} />,
  },
];
