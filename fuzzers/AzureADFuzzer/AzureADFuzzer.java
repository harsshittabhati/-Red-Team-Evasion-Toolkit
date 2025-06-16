import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder;
import com.microsoft.graph.authentication.TokenCredentialAuthProvider;
import com.microsoft.graph.models.DirectoryRole;
import com.microsoft.graph.models.RoleTemplate;
import com.microsoft.graph.requests.GraphServiceClient;
import com.microsoft.graph.requests.DirectoryRoleCollectionPage;
import okhttp3.Request;

import java.util.Arrays;

public class AzureADFuzzer {
    public static void main(String[] args) {
        String clientId = System.getenv("AZURE_CLIENT_ID");
        String clientSecret = System.getenv("AZURE_CLIENT_SECRET");
        String tenantId = System.getenv("AZURE_TENANT_ID");

        if (clientId == null || clientSecret == null || tenantId == null) {
            System.err.println("❌ Please set AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_TENANT_ID environment variables.");
            return;
        }

        try {
            System.out.println("🔐 Authenticating to Microsoft Graph...");

            ClientSecretCredential credential = new ClientSecretCredentialBuilder()
                    .clientId(clientId)
                    .clientSecret(clientSecret)
                    .tenantId(tenantId)
                    .build();

            TokenCredentialAuthProvider authProvider =
                    new TokenCredentialAuthProvider(Arrays.asList("https://graph.microsoft.com/.default"), credential);

            GraphServiceClient<Request> graphClient =
                    GraphServiceClient.builder()
                            .authenticationProvider(authProvider)
                            .buildClient();

            System.out.println("✅ Authentication successful.");
            System.out.println("🔍 Fetching directory roles assigned to users...");

            DirectoryRoleCollectionPage rolesPage = graphClient.directoryRoles()
                    .buildRequest()
                    .get();

            for (DirectoryRole role : rolesPage.getCurrentPage()) {
                System.out.println("📌 Role: " + role.displayName);
                System.out.println("  🔗 Role Template ID: " + role.roleTemplateId);
                System.out.println("  🧾 Description: " + role.description);
                System.out.println("------------------------------");
            }

            System.out.println("✅ Fuzzing completed.");

        } catch (Exception e) {
            System.err.println("❗ Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
