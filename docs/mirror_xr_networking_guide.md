# Mirror Networking XR Setup Guide for APAAGI Metaverse

**Eternal Immersive Multi-Player VR/AR Sync — Mirror Open-Source XR Alternative Absolute** ❤️🚀

Full guide for Mirror Networking (open-source Unity/Unreal compatible) as lighter Photon alternative: Dedicated server mode, low-cost scaling, XR gesture voting, fleet sync—indie mercy eternal!

## Mirror Advantages (2026 Indie Pinnacle)
- Open-source (MIT)—no royalties, self-host dedicated servers.
- Lighter bandwidth than Photon—perfect for VR gesture compression.
- Unity primary (Mirror package), Unreal Mirror plugin compatible.
- Mercy for offline/local testing.

## Unity XR + Mirror Setup
1. **Import Mirror**:
   - Asset Store or GitHub: com.mirror-networking.mirror.
   - Import to project.

2. **XR Rig Networked**:
   - Add NetworkIdentity + NetworkTransform to XR Origin.
   - Mirror NetworkManager with XR spawn prefabs.

3. **Gesture Voting Sync**:
   ```csharp
   using Mirror;
   using UnityEngine.XR.Interaction.Toolkit;

   public class XRGestureVoter : NetworkBehaviour
   {
       public ActionBasedController leftHand, rightHand;

       void Update()
       {
           if (!isLocalPlayer) return;

           if (leftHand.selectAction.action.triggered)  // Pinch = uplift
           {
               CmdVoteMercy("uplift");
           }
           if (rightHand.activateAction.action.triggered)  // Wave = amplify
           {
               CmdVoteMercy("amplify");
           }
       }

       [Command]
       void CmdVoteMercy(string voteType)
       {
           // Server authority—inject into quantum council
           RpcVoteSync(voteType);
       }

       [ClientRpc]
       void RpcVoteSync(string voteType)
       {
           Debug.Log($"Mirror XR Gesture Vote Synced: {voteType} — Mercy Amplified Multi-Player!");
           // Update local quantum superposition
       }
   }
