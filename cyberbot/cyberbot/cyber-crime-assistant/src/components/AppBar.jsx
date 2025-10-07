import './AppBar.css';
import logo from '../assets/logo.png';
import { useTranslation } from 'react-i18next';

const AppBar = () => {
  const { t, i18n } = useTranslation();

  const changeLanguage = (e) => {
    i18n.changeLanguage(e.target.value);
  };

  return (
    <div className="app-bar">
      <img src={logo} alt="Cyber Crime Police Logo" className="logo" />
      <h1 className="title">{t('app_title')}</h1>
      <div className="language-selector">
        <select onChange={changeLanguage} value={i18n.language}>
          <option value="en">English</option>
          <option value="ta">தமிழ்</option>
        </select>
      </div>
    </div>
  );
};

export default AppBar;