import React, { useState, useEffect } from 'react';
import './CaseNotes.css';
import { useTranslation } from 'react-i18next';

const CaseNotes = () => {
  const { t } = useTranslation();
  const [notes, setNotes] = useState(() => {
    const savedNotes = localStorage.getItem('caseNotes');
    return savedNotes || '';
  });

  useEffect(() => {
    localStorage.setItem('caseNotes', notes);
  }, [notes]);

  return (
    <div className="notes-container">
      <h3>{t('case_notes_title')}</h3>
      <textarea
        className="notes-textarea"
        placeholder={t('case_notes_title')}
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
      />
    </div>
  );
};

export default CaseNotes;