using UnityEngine;
using System;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;

namespace Quiz
{
    public class RequestQuizData : MonoBehaviour
    {
        private const float TIMEOUT_SECONDS = 5f;
        public string hostURL = "";
        public string classId = "";


        public IEnumerator GetQuizReport()
        {
            string fullUrl = hostURL + "class/" + classId + "/report";
            Uri uriInfo = new Uri(fullUrl);

            Debug.Log($"[API 요청 시작] URL: {fullUrl}");
            Debug.Log($"[서버 정보] Scheme: {uriInfo.Scheme}, Host: {uriInfo.Host}, Port: {uriInfo.Port}, Path: {uriInfo.AbsolutePath}");

            using (UnityWebRequest webRequest = new UnityWebRequest(fullUrl, "GET"))
            {
                // 타임아웃 설정
                webRequest.timeout = (int)TIMEOUT_SECONDS;

                // 요청 시작 시간 기록
                float startTime = Time.time;
                webRequest.downloadHandler = new DownloadHandlerBuffer();
                webRequest.SetRequestHeader("Content-Type", "application/json");
                webRequest.useHttpContinue = true;
                webRequest.SetRequestHeader("withCredentials", "true");

                // HTTP 비보안 연결 허용 설정
                yield return webRequest.SendWebRequest();

                // 응답 시간 체크
                float responseTime = Time.time - startTime;
                if (responseTime >= TIMEOUT_SECONDS)
                {
                    Debug.LogError($"[타임아웃 오류] 응답 시간: {responseTime:F2}초 (제한: {TIMEOUT_SECONDS}초)");
                    yield break;
                }

                switch (webRequest.result)
                {
                    case UnityWebRequest.Result.ConnectionError:
                        Debug.LogError($"[연결 오류]\n오류 내용: {webRequest.error}\n상세 내용: {webRequest.downloadHandler?.text}");
                        Debug.LogError(webRequest.responseCode);
                        break;
                    case UnityWebRequest.Result.DataProcessingError:
                        Debug.LogError($"[데이터 처리 오류]\n오류 내용: {webRequest.error}\n상세 내용: {webRequest.downloadHandler?.text}");
                        break;
                    case UnityWebRequest.Result.ProtocolError:
                        Debug.LogError($"[HTTP 프로토콜 오류]\n상태 코드: {webRequest.responseCode}\n오류 내용: {webRequest.error}\n상세 내용: {webRequest.downloadHandler?.text}");
                        break;
                    case UnityWebRequest.Result.Success:
                        Debug.Log("[요청 성공]");
                        Debug.Log($"[응답 데이터]\n{webRequest.downloadHandler.text}");
                        // StudentQuizResponse response = JsonUtility.FromJson<StudentQuizResponse>(webRequest.downloadHandler.text);
                        // Managers.Quiz.SetSolveQuizData(response.data.quizzesByStageAndStep);
                        break;
                }
            }
        }
        public IEnumerator GetQuizData()
        {
            string fullUrl = hostURL + "class/" + classId + "/student";
            Uri uriInfo = new Uri(fullUrl);

            Debug.Log($"[API 요청 시작] URL: {fullUrl}");
            Debug.Log($"[서버 정보] Scheme: {uriInfo.Scheme}, Host: {uriInfo.Host}, Port: {uriInfo.Port}, Path: {uriInfo.AbsolutePath}");

            using (UnityWebRequest webRequest = new UnityWebRequest(fullUrl, "GET"))
            {
                // 타임아웃 설정
                webRequest.timeout = (int)TIMEOUT_SECONDS;

                // 요청 시작 시간 기록
                float startTime = Time.time;
                webRequest.downloadHandler = new DownloadHandlerBuffer();
                webRequest.SetRequestHeader("Content-Type", "application/json");
                webRequest.useHttpContinue = true;
                webRequest.SetRequestHeader("withCredentials", "true");
                // HTTP 비보안 연결 허용 설정
                yield return webRequest.SendWebRequest();

                // 응답 시간 체크
                float responseTime = Time.time - startTime;
                if (responseTime >= TIMEOUT_SECONDS)
                {
                    Debug.LogError($"[타임아웃 오류] 응답 시간: {responseTime:F2}초 (제한: {TIMEOUT_SECONDS}초)");
                    yield break;
                }

                switch (webRequest.result)
                {
                    case UnityWebRequest.Result.ConnectionError:
                        Debug.LogError($"[연결 오류]\n오류 내용: {webRequest.error}\n상세 내용: {webRequest.downloadHandler?.text}");
                        break;
                    case UnityWebRequest.Result.DataProcessingError:
                        Debug.LogError($"[데이터 처리 오류]\n오류 내용: {webRequest.error}\n상세 내용: {webRequest.downloadHandler?.text}");
                        break;
                    case UnityWebRequest.Result.ProtocolError:
                        Debug.LogError($"[HTTP 프로토콜 오류]\n상태 코드: {webRequest.responseCode}\n오류 내용: {webRequest.error}\n상세 내용: {webRequest.downloadHandler?.text}");
                        break;
                    case UnityWebRequest.Result.Success:
                        Debug.Log("[요청 성공]");
                        Debug.Log($"[응답 데이터]\n{webRequest.downloadHandler.text}");
                        // RootResponse response = JsonUtility.FromJson<RootResponse>(webRequest.downloadHandler.text);
                        // for (int i = 0; i < response.data.courseContent.courseContentDetails.Count; i++)
                        // {
                        //     if (response.data.courseContent.courseContentDetails[i].activityStage == "EXPERIMENT")
                        //     {
                        //         Managers.Quiz.SetQuizData(response.data.courseContent.courseContentDetails[i]);
                        //     }
                        // }
                        break;
                }
            }
        }
        public void GetReport()
        {
            StartCoroutine(GetQuizReport());
        }
        public void GetData()
        {
            StartCoroutine(GetQuizData());
            StartCoroutine(GetQuizReport());
        }

    }
}

