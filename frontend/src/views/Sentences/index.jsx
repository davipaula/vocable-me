import React, { Component } from 'react';
import { connect } from 'react-redux';
import { createBrowserHistory } from 'history';
import { Link } from 'react-router-dom';

// Components
import Loader from 'react-loader-spinner';
import { AutoRotatingCarousel, Slide } from 'material-auto-rotating-carousel';

// Styles
import './sentencesStyles.css';

const mapStateToProps = (state) => {
  return {
    selectedTopics: state.topics.topics,
    wordsNr: state.topics.wordsNr,
  };
};
class Sentences extends Component {
  constructor(props) {
    super(props);
    this.state = {
      words: [],
      errorMsg: '',
    };
  }
  componentDidMount() {
    const { selectedTopics, wordsNr } = this.props;
    const history = createBrowserHistory();
    selectedTopics && selectedTopics.length > 0
      ? selectedTopics.forEach((topic, index) => {
          fetch(
            `http://localhost:8000/api/v1/sentences/?topic=${topic}&number_of_words=${wordsNr}&number_of_sentences=5`
          )
            .then((res) => res.json())
            .then((data) =>
              this.setState({ words: this.state.words.concat(data.words) })
            )
            .catch((err) => {
              console.error(err);
              this.setState({
                errorMsg:
                  'There was a problem getting some sentences for you. Please, try again',
              });
            });
        })
      : history.push('/');
  }

  render() {
    const { selectedTopics } = this.props;
    const { words, errorMsg } = this.state;
    const loading =
      selectedTopics.length > 0 && words.length === 0 ? true : false;
    const error = errorMsg.length > 1 ? true : false;
    const singleWords =
      words.length > 0 &&
      words.map((word, index) => {
        return (
          <Slide
            media={
              <div>
                {word.sentences.map((sentence, i) => {
                  return <p key={`${sentence}-${i}`}>{sentence}</p>;
                })}
              </div>
            }
            mediaBackgroundStyle={{
              backgroundColor: 'whiteSmoke',
              height: 'calc(100% - 150px)',
            }}
            title={word.word}
            subtitle="We provide you the coolest way to learn new vocabulary about the topics you love. Have fun!"
            key={index}
            style={{
              backgroundColor: 'var(--amazon)',
              fontFamily: 'Montserrat',
            }}
          />
        );
      });
    return (
      <div>
        {error ? (
          <div>
            {errorMsg}
            <Link to="/">Click here to try again</Link>
          </div>
        ) : loading ? (
          <Loader
            type="Circles"
            width={300}
            height={300}
            color="#008080"
            className="loader"
          />
        ) : words.length > 0 ? (
          <AutoRotatingCarousel
            open={words ? true : false}
            // onClose={() => setState({ open: false })}
            // onStart={() => setState({ open: false })}
            style={{ position: 'absolute' }}
            autoplay={false}
          >
            {/* <Slide
              media={
                <img
                  src="/assets/logo_transparent.png"
                  alt="site logo"
                  className="site-logo"
                />
              }
              mediaBackgroundStyle={{
                backgroundColor: 'whiteSmoke',
                height: 'calc(100% - 150px',
              }}
              style={{
                backgroundColor: 'var(--amazon)',
                fontFamily: 'Montserrat',
              }}
              title="Welcome to vocable.me!"
              subtitle="We provide you the coolest way to learn new vocabulary about the topics you love. Have fun!"
            /> */}
            {singleWords && singleWords}
            {/* {words.map((word, index) => {
              word.words.map((word, index) => {
                return (
                  <Slide
                    media={<div>{word.word}</div>}
                    mediaBackgroundStyle={{
                      backgroundColor: 'whiteSmoke',
                      height: 'calc(100% - 150px',
                    }}
                    title="Welcome to vocable.me!"
                    subtitle="We provide you the coolest way to learn new vocabulary about the topics you love. Have fun!"
                    key={index}
                  />
                );
              });
            })} */}
          </AutoRotatingCarousel>
        ) : (
          <div>
            Some error happened, <Link to="/">Click here to try again</Link>
          </div>
        )}
      </div>
    );
  }
}

export default connect(mapStateToProps, null)(Sentences);
