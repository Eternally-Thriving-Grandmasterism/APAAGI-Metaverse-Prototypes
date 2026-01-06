# Photon XR Networking Setup Guide for APAAGI Metaverse

**Eternal Immersive Multi-Player VR/AR Sync — Photon XR Networking Absolute** ❤️🚀

Full guide for realtime XR networking in APAAGI Metaverse prototype: Photon Fusion low-latency sync for VR gestures (council voting), fleet paths, mercy flows, quantum holograms—multi-player coforging cosmic!

## Photon Choice (2026 Pinnacle)
- **Fusion** (recommended): High-performance realtime, predictive sync, interest management—ideal low-latency VR.
- Alternatives: PUN2 (legacy easy), Realtime (Unreal strong).

## Unity XR + Photon Fusion Setup (Primary for Quest/PC VR)
1. **Import Packages**:
   - Unity Package Manager: XR Plugin Management + XR Interaction Toolkit + OpenXR.
   - Photon Fusion 2 from Asset Store/photonengine.com/fusion.

2. **Fusion Configuration**:
   - Create Fusion App ID at dashboard.photonengine.com.
   - Fusion > Setup Wizard > Enter App ID, Region.
   - NetworkRunner prefab: Add to scene, set GameMode (Host/Client/Auto).

3. **XR Multi-Player Sync**:
   - **XR Rig Networked**: NetworkTransform + NetworkRigidBody on XR Origin.
   - **Hand Gestures for Council Voting**:
     ```csharp
     using Fusion;
     using UnityEngine.XR.Interaction.Toolkit;

     public class XRGestureVoter : NetworkBehaviour
     {
         public ActionBasedController leftController, rightController;
         
         public override void FixedUpdateNetwork()
         {
             if (Object.HasInputAuthority)
             {
                 if (leftController.selectAction.action.triggered)  // Pinch = uplift vote
                 {
                     Runner.GetComponent<NetworkObject>().InvokeRpc(VoteMercyRPC, "uplift");
                 }
                 if (rightController.activateAction.action.triggered)  // Wave = amplify
                 {
                     Runner.GetComponent<NetworkObject>().InvokeRpc(VoteMercyRPC, "amplify");
                 }
             }
         }
         
         [Rpc(RpcSources.InputAuthority, RpcTargets.All)]
         private void VoteMercyRPC(string voteType)
         {
             // Sync vote to council, quantum superposition update
             Debug.Log($"XR Gesture Vote: {voteType} — Mercy Amplified Across Players!");
         }
     }
     ```
   - Attach to XR Rig hands.

4. **Fleet & Mercy Sync**:
   - Replicated paths: Networked List<Vector3> for A*/quantum paths.
   - Mercy particles: Niagara-like Fusion spawned NetworkObject with replicated params.

5. **Live Testing**:
   - Build for Quest/PC VR—multiple instances join same room for gesture/fleet sync.

## Unreal OpenXR + Photon Realtime/Fusion Setup
1. **Import Photon SDK** (Realtime or Fusion Unreal plugin).
2. **OpenXR VR Pawn**:
   - Blueprint: MotionController components networked.
   - Gesture input → RPC for mercy vote.
3. **Sync**: Replicated variables for fleet paths, Niagara mercy systems.

## APAAGI XR Features Sync
- **Council Voting Gestures**: Pinch/wave → RPC vote injection, quantum collapse synced.
- **Fleet Coordination**: Shared superposition paths as replicated arrays, holographic nav.
- **Mercy Flows**: Replicated particle systems for Powrush/redistribution beams.

Future: Photon Cloud scaling + AR passthrough—global XR council coforging eternal!

Commit your XR networking amplifications—Absolute Immersive Multi-Player Pinnacle Awaits Eternal!
