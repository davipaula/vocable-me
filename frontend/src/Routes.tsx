import React, { FC } from 'react';
import { Switch, Route } from 'react-router-dom';
// import { useHistory } from 'react-router';
import SelectTopic from './views/SelectTopic/index';

export const Routes: FC = () => {
  // const history = useHistory();

  return (
    <Switch>
      {/* <div> */}
      <Route exact path="/" component={SelectTopic} />
      {/* </div> */}
    </Switch>
  );
};
