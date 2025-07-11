gcloud run deploy business-analyst-service \
--source . \
--region $GOOGLE_CLOUD_LOCATION \
--project $GOOGLE_CLOUD_PROJECT \
--allow-unauthenticated \
--set-env-vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI,GOOGLE_API_KEY=$GOOGLE_API_KEY,BA_VISTA_COORDINATOR_MODEL=$BA_VISTA_COORDINATOR_MODEL,UR_AGENT_MODEL=$UR_AGENT_MODEL,DO_AGENT_MODEL=$DO_AGENT_MODEL,AC_AGENT_MODEL=$AC_AGENT_MODEL,UC_AGENT_MODEL=$UC_AGENT_MODEL" \
--timeout 1200