import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { About } from "../components/about/about";
import { Menu } from "../components/Menu/Menu";
import { Main } from "../components/Main/Main";
import { PvadminLogin } from "../components/Pvadmin/PVLogin";
import { Eventos } from "../components/Eventos/Eventos";
import { NewsList } from "../components/Feed/Feed";
import { UsersList } from "../components/Pvadmin/PVUsers";

function App() {
  return (
    <Router>
      <Menu />
      <div className="container">
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/pvadmin/loginv2" element={<PvadminLogin />} />
          <Route path="/pvadmin/all-usersv2" element={<UsersList />} />
          <Route path="/eventos" element={<Eventos />} />
          <Route path="/About" element={<About />} />
          <Route path="/notices" element={<NewsList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
