// MCP Unity 서버 자동 시작 & Cursor 설정 자동 적용 스크립트
// 최초 1회만 실행됨

using UnityEditor;

[InitializeOnLoad]
public static class McpAutoSetup
{
    // EditorPrefs에 저장할 키값 (중복 실행 방지)
    private const string c_McpAutoSetupKey = "McpAutoSetup_Executed";


    static McpAutoSetup()
    {
        // 이미 실행된 적 있으면 아무것도 하지 않음
        if (EditorPrefs.GetBool(c_McpAutoSetupKey, false))
            return;

        // MCP 서버 자동 시작
        McpUnityServer.Instance.StartServer();

        // Cursor 설정 자동 적용 (탭 인덴트 사용 여부는 false/true로 선택)
        McpConfigUtils.AddToCursorConfig(false);

        // 최초 1회 실행 완료 표시
        EditorPrefs.SetBool(c_McpAutoSetupKey, true);

        // 실행 결과 안내 (콘솔)
        UnityEngine.Debug.Log("[MCP] MCP 서버 자동 시작 & Cursor 설정 자동 적용 완료 (최초 1회만 실행)");
    }
}