import React from 'react';
import './EvidenceChecklist.css';
import { useTranslation } from 'react-i18next';

const EvidenceChecklist = ({ checklist }) => {
  const { t } = useTranslation();
  
  return (
    <div className="checklist-container">
      <h3>{t('evidence_checklist_title')}</h3>
      {checklist.length > 0 ? (
        <ul>
          {checklist.map((item, index) => (
            <li key={index}>
              <input type="checkbox" id={`checklist-item-${index}`} />
              <label htmlFor={`checklist-item-${index}`}>{item}</label>
            </li>
          ))}
        </ul>
      ) : (
        <p className="no-items-message">{t('no_checklist_items')}</p>
      )}
    </div>
  );
};

export default EvidenceChecklist;