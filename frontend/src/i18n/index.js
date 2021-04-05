import i18n from 'i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import { en, br } from './locales';
import { initReactI18next } from 'react-i18next';

const options = {
  interpolation: {
    escapeValue: false, // not needed for react
    format: (value, format, lng) => {
      if (format === 'intlDate') {
        return new Intl.DateTimeFormat(lng).format(value);
      }
      return value;
    },
  },
  formattedDate: '{{date, intlDate}}',
  debug: false,
  // The line below is needed when not using language detector feature. It sets default language to english.
  //lng: 'en',

  resources: {
    br: {
      common: br.br,
    },
    en: {
      common: en.en,
    },
  },
  fallbackLng: 'en',
  ns: ['common'],
  defaultNS: 'common',
  react: {
    wait: false,
    bindI18n: 'languageChanged loaded',
    bindStore: 'added removed',
    nsMode: 'default',
  },
};
i18n.use(initReactI18next).use(LanguageDetector).init(options);
// .changeLanguage('en', (err, t) => {
//   if (err) return console.log('something went wrong loading', err);
// });

export default i18n;

export const getCurrentLocale = (complete = false) => {
  var locale = localStorage.getItem('i18nextLng');
  if (complete) return locale;
  return locale ? locale.split('-')[0] : null;
};
