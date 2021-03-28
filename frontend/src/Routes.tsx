import React, { FC } from 'react';
import { Switch, Route } from 'react-router-dom';
// import { useHistory } from 'react-router';
import SelectTopic from './views/SelectTopic/index';
import Sentences from './views/Sentences/index';

export const Routes: FC = () => {
  // const history = useHistory();

  return (
    <Switch>
      {/* <div> */}
      <Route exact path="/" component={SelectTopic} />
      <Route exact path="/sentences" component={Sentences} />
      {/* </div> */}
    </Switch>
  );
};
