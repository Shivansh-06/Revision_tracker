import { apiFetch } from "./client";

/* ===============================
   REVISION QUEUE
================================ */

export function getUnitWiseRevisionQueue(token, mode = null) {
  const query = mode ? `?mode=${mode}` : "";
  return apiFetch(`/revision-queue/unit-wise${query}`, { token });
}

/* ===============================
   MARK REVISED
================================ */

export function markTopicRevised(token, topicId) {
  return apiFetch(`/revisions/${topicId}/mark`, {
    method: "POST",
    token,
  });
}

export function markUnitRevised(token, subject, unit) {
  return apiFetch(
    `/revisions/unit/mark`,
    {
      method: "POST",
      token,
      body: { subject, unit },
    }
  );
}

/* ===============================
   STREAKS
================================ */

export function getStreak(token) {
  return apiFetch("/revisions/streak", { token });
}

/* ===============================
   DAILY GOALS
================================ */

export function getDailyGoal(token) {
  return apiFetch("/revisions/daily-goal", { token });
}

export function getAdaptiveDailyGoal(token) {
  return apiFetch("/revisions/daily-goal/subject", { token });
}

/* ===============================
   ANALYTICS
================================ */

export function getWeeklySummary(token) {
  return apiFetch("/revisions/weekly-summary", { token });
}

export function getSubjectWeeklySummary(token) {
  return apiFetch("/revisions/weekly-summary/subject", { token });
}

export function getSubjectBalance(token) {
  return apiFetch("/revisions/subject-balance", { token });
}

/* ===============================
   TOPICS
================================ */ 
export function getTopics(token) {
    return apiFetch("/topics", { token });  
}

export function addRevision(token, topicId, confidence) {
    return apiFetch(`/revisions`, {
        method: "POST",
        token,
        body: {
            topic_id: topicId,
            confidence: confidence || 3,
        },
    });
}

/* ===============================
   PRIORITY MODES
================================ */
export function getPriorityModes(token) {
    return apiFetch("/priority-modes", { token });
}

export function setPriorityMode(token, mode) {
    return apiFetch("/revisions/priority-mode", {
        method: "POST",
        token,
        body: { mode },
    });
}

/* ===============================
   REVISION SETTINGS
================================ */
export function getRevisionSettings(token) {
    return apiFetch("/revision-settings", { token });
}

export function setRevisionSettings(token, settings) {
    return apiFetch("/revision-settings", {
        method: "POST",
        token,
        body: settings,
    });
}

/* ===============================
   ADD TOPIC
================================ */
export function addTopic(token, topicData) {
    return apiFetch("/topics", {
        method: "POST",
        token,
        body: topicData,
    });
}

/* ===============================
   DELETE TOPIC
================================ */
export function deleteTopic(token, topicId) {
    return apiFetch(`/topics/${topicId}`, {
        method: "DELETE",
        token,
    });
}

/* ===============================
   EDIT TOPIC
================================ */
export function editTopic(token, topicId, topicData) {
    return apiFetch(`/topics/${topicId}`, {
        method: "PUT",
        token,
        body: topicData,
    });
}

/* ===============================
   SEARCH TOPICS
================================ */
export function searchTopics(token, query) {
    return apiFetch(`/topics/search?q=${encodeURIComponent(query)}`, { token });
}

/* ===============================
   BULK INSERT TOPICS
================================ */
export function bulkCreateTopics(token, topics) {
    return apiFetch("/topics/bulk", {
        method: "POST",
        token,
        body: { topics },
    });
}

/* ===============================
   SYLLABUS PARSING
================================ */     
export function parseSyllabus(token, text, subject = null) {
    return apiFetch("/syllabus/parse", {
        method: "POST",
        token,
        body: { text, subject },
    });
}

/* ===============================
   IMPORT SYLLABUS
================================ */
export function importSyllabus(token, syllabusData) {
    return apiFetch("/syllabus/import", {
        method: "POST",
        token,
        body: syllabusData,
    });
}

/* ===============================
   EXPORT SYLLABUS
================================ */
export function exportSyllabus(token) {
    return apiFetch("/syllabus/export", { token });
}


/* ===============================
   EXPORT REVISION DATA
================================ */
export function exportRevisionData(token) {
    return apiFetch("/revisions/export", { token });
}

/* ===============================
   IMPORT REVISION DATA
================================ */
export function importRevisionData(token, revisionData) {
    return apiFetch("/revisions/import", {
        method: "POST",
        token,
        body: revisionData,
    });
}

/* ===============================
   RESET REVISION DATA
================================ */
export function resetRevisionData(token) {
    return apiFetch("/revisions/reset", {
        method: "POST",
        token,
    });
}

/* ===============================
    RESET SYLLABUS DATA
================================ */
export function resetSyllabusData(token) {
    return apiFetch("/syllabus/reset", {
        method: "POST",
        token,
    });
}

/* ===============================
   CLEAR COMPLETED REVISIONS
================================ */
export function clearCompletedRevisions(token) {    
    return apiFetch("/revisions/clear-completed", {
        method: "POST",
        token,
    });
}

/* ===============================
   GET SUBJECTS
================================ */
export function getSubjects(token) {
    return apiFetch("/subjects", { token });
}

/* ===============================
   GET UNITS
================================ */
export function getUnits(token, subject) {
    return apiFetch(`/subjects/${encodeURIComponent(subject)}/units`, { token });
}


/* ===============================
   GET TOPICS BY UNIT
================================ */

export function getTopicsByUnit(token, subject, unit) {
    return apiFetch(
        `/subjects/${encodeURIComponent(subject)}/units/${encodeURIComponent(unit)}/topics`,
        { token }
    );
}

/* ===============================
   GET TOPIC DETAILS
================================ */
export function getTopicDetails(token, topicId) {
    return apiFetch(`/topics/${topicId}`, { token });
}

/* ===============================
   ADD MULTIPLE REVISIONS
================================ */
export function addMultipleRevisions(token, topicId, count) {
    return apiFetch(`/topics/${topicId}/add-multiple-revisions`, {
        method: "POST",
        token,
        body: { count },
    });
}

/* ===============================
   DELETE REVISION
================================ */

export function deleteRevision(token, revisionId) {
    return apiFetch(`/revisions/${revisionId}`, {
        method: "DELETE",
        token,
    });
}

/* ===============================
   EDIT REVISION
================================ */
export function editRevision(token, revisionId, revisionData) {
    return apiFetch(`/revisions/${revisionId}`, {
        method: "PUT",
        token,
        body: revisionData,
    });
}

/* ===============================
    GET REVISION DETAILS    
================================ */
export function getRevisionDetails(token, revisionId) {
    return apiFetch(`/revisions/${revisionId}`, { token });
}   

/* ===============================
   SEARCH REVISIONS
================================ */
export function searchRevisions(token, query) {
    return apiFetch(`/revisions/search?q=${encodeURIComponent(query)}`, { token });
}

/* ===============================
   GET REVISION QUEUE
================================ */
export function getRevisionQueue(token, mode = null) {
    const query = mode ? `?mode=${mode}` : "";
    return apiFetch(`/revision-queue${query}`, { token });
}


