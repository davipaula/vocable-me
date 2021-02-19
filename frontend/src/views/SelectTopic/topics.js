import React from 'react';

// Icons
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

// i18n
import i18n from '../../i18n/index';

export const topics = [
  {
    label: i18n.t('topics.culinary'),
    icon: <FontAwesomeIcon icon={['fas, fa-utensils']} />,
  },
  {
    label: i18n.t('topics.business'),
    icon: <FontAwesomeIcon icon={['fas, fa-user-tie']} />,
  },
  {
    label: i18n.t('topics.technology'),
    icon: <FontAwesomeIcon icon={['fas, fa-laptop-code']} />,
  },
  {
    label: i18n.t('topics.movies'),
    icon: <FontAwesomeIcon icon={['fas, fa-film']} />,
  },
  {
    label: i18n.t('topics.music'),
    icon: <FontAwesomeIcon icon={['fas, fa-guitar']} />,
  },
  {
    label: i18n.t('topics.politics'),
    icon: <FontAwesomeIcon icon={['fas, fa-handshake']} />,
  },
  {
    label: i18n.t('topics.sports'),
    icon: <FontAwesomeIcon icon={['fas, fa-dumbbell']} />,
  },
  {
    label: i18n.t('topics.literature'),
    icon: <FontAwesomeIcon icon={['fas, fa-book']} />,
  },
  {
    label: i18n.t('topics.law'),
    icon: <FontAwesomeIcon icon={['fas, fa-balance-scale']} />,
  },
];
