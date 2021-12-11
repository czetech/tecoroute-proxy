{{/*
Expand the name of the chart.
*/}}
{{- define "tecoroute-proxy.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 46 chars because some Kubernetes name fields are limited to this
(by the DNS naming spec) with a 17-character reservation for the component
name. If release name contains chart name it will be used as a full name.
*/}}
{{- define "tecoroute-proxy.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 46 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 46 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 46 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "tecoroute-proxy.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "tecoroute-proxy.labels" -}}
helm.sh/chart: {{ include "tecoroute-proxy.chart" . }}
{{ include "tecoroute-proxy.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "tecoroute-proxy.selectorLabels" -}}
app.kubernetes.io/name: {{ include "tecoroute-proxy.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
