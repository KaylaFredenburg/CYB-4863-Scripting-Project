# Group 1: Scripting Assignment

**Kayla Fredenburg, Mahin Moon, Alexis Watson, Benton Raymer, Xingzhou Li, Matthew Adams**  
**03/02/2025**

## Introduction

Research indicates cybersecurity incidents significantly impact organizations' financial stability, customer retention, and reputation (W. Li et al., 2023; Schlackl et al., 2022; Woods and Bohme, 2021). Both the frequency and intensity of incidents continue to escalate (Romanosky, 2016; Schlackl et al., 2022) while companies continually struggle in a cybersecurity arms race with attackers. Social engineering and phishing are commonly used to infiltrate companies' defense mechanisms, resulting in malware, specifically ransomware, and often data breaches. 

This report presents a System Inventory and Security Audit Tool designed to collect essential system data, including active users, installed software, missing security patches, and USB device history. This tool uses Python to automate data extraction, leveraging subprocess commands, Windows Registry queries, and log file analysis to generate a comprehensive system report. 

Automated detection of security gaps enhances system monitoring by improving scalability, speed, and efficiency, helping to mitigate potential threats and incidents. This report will review the methodology, code structure, and results, demonstrating how the tool efficiently gathers and organizes system security information.

## Scripts Used

### Preparation Script
[Asset Inventory Script](https://github.com/KaylaFredenburg/CYB-4863-Scripting-Project/blob/main/Asset%20Inventory%20Script.py)

### Detection Script
[SuspiciousLoginMonitoring.py](https://github.com/KaylaFredenburg/CYB-4863-Scripting-Project/blob/main/SuspiciousLoginMonitoring.py)

## Findings

### System Information Gathering
[AssetInventoryOutput.json](https://github.com/KaylaFredenburg/CYB-4863-Scripting-Project/blob/main/AssetInventoryOutput.json)

### Failed Login Attempts Detection
[login-script-output.png](https://github.com/KaylaFredenburg/CYB-4863-Scripting-Project/blob/main/login-script-output.png)

## Reflections

### Benefits of Automation

The benefits of automating a system are vast, yet they focus mainly on creating a system that runs continually and reducing potential human error. 

Human error is a recurring theme in cybersecurity—social engineering and phishing are two of the most common methods of entry. Automation helps reduce the possibility of human error within the detection phase of any system's security framework. Automating the detection of malicious events allows for continuous monitoring, while automated notifications ensure that security teams are alerted based on the severity of an incident.

Thus, automation strengthens the consistency of detection and response systems. Consistency is integral—by ensuring repeatable and accurate results, malicious behavior and potential compromise can be identified and mitigated before it spreads. 

For instance, in the Preparation Phase, an automated asset inventory script can ensure that all systems are accounted for before an incident occurs. This script can systematically list all active users, identify installed software and versions, and check for missing security patches, ensuring the security team has a relevant overview of the system. Manual asset tracking is prone to human error-caused oversight; however, automation guarantees that critical security gaps—such as outdated software or unauthorized user accounts—are flagged and addressed promptly.

By having automated detection and response systems running continuously, organizations are protected from threats that may arise outside of standard working hours when SOC teams are unavailable. Many organizations have begun implementing structured schedules for SOC workers to prevent burnout, ensuring that human analysts remain sharp and effective. However, security threats do not adhere to the company's business hours. 

An example of how automation benefits the Detection Phase is an automated suspicious login monitoring script that can provide continuous oversight by parsing system logs for failed login attempts, identifying repeated failures from the same IP, and triggering alerts when a predefined threshold is exceeded. Without automation, SOC teams would have to sift through logs manually, which is time-consuming and inefficient. By implementing an automated solution, security teams can ensure that brute-force attempts and unauthorized access are detected in real time, regardless of when they occur.

Automation also benefits security professionals due to the increased speed at which tasks can be performed. Once a script is created, the associated task can be executed efficiently moving forward (albeit with upkeep). For example, a Python script designed to check for missing security patches can be deployed across an entire network within minutes, but manually verifying patch status across multiple endpoints is inefficient. The improved speed of automated detection and response ensures that vulnerabilities are addressed promptly before being exploited.

Once an automated system is developed, it can be stored, refined, and reused across different scenarios. This reusability fortifies defenses against potential future incidents and enhances the organization's ability to scale security operations. For example, the asset inventory script developed in the Preparation Phase can be scheduled to run periodically, ensuring continuous monitoring of system configurations as the organization grows. Likewise, the suspicious login monitoring script can be expanded to integrate with SIEM solutions, allowing for greater scalability as more logs and user behaviors must be analyzed. Automation ensures that security frameworks remain effective and adaptable as organizations scale, preventing bottlenecks in security operations.

By leveraging automation in preparation and detection, organizations can significantly improve their cybersecurity defenses' speed, consistency, efficiency, and scalability. This minimizes human error and enables security teams to focus on complex, high-value threats while automated processes handle routine but critical security tasks.

## Lessons Learned

Observing other groups' implementations provided insight into potential improvements. The use of command-line arguments allowed for dynamic script execution, enabling users to select features or parameters at runtime—a simple yet effective enhancement that would add flexibility to our tool. Another notable approach was in reporting methodologies. Our login monitoring script currently checks every minute and provides a summary of issues over the last 10 minutes, but some teams opted to output results only when a problem occurred, reducing unnecessary logs. Implementing this as a command-line argument would allow users to choose their preferred functionality. Additionally, while our script outputs data to a text file, using JSON would make it more structured and easier for further automation. These refinements would improve usability and adaptability, ensuring the tool remains scalable and efficient.

Additionally, another way to improve our program was to implement a hybrid approach. The Windows information-gathering script, developed solely Python, automates system data collection by tracking active users, installed software, and missing security patches, ultimately improving security oversight while minimizing human error. However, integrating PowerShell for patch identification could significantly enhance its accuracy and efficiency. Unlike Python, PowerShell offers native Windows integration, allowing real-time assessment of patch status through commands such as Get-WindowsUpdate or Microsoft's Update Compliance API. While Python provided cross-platform flexibility, PowerShell could enable more advanced methods, such as analyzing Windows Update logs via Get-WindowsUpdateLog, leveraging Get-WUList from the Windows Update Module to compare installed patches against available updates, and offering a deeper insight into update failures. These enhancements would provide a more comprehensive view of missing security updates rather than simply listing currently installed ones.


## Conclusion

Part 1 of the project shows a tool that successfully gathered key system data, including active users, installed software, missing security patches, and USB device history. This information provided an overview of system health and security, helping to identify vulnerabilities such as missing patches and potential security gaps related to USB devices. The automated process ensured that this data was collected efficiently and consistently, removing human error and reducing the workload for IT teams, increasing both their speed and efficiency.

Part 2 shows a brute-force detection tool that can identify potential security threats through failed login attempts. Alerts were triggered for potential brute-force attacks, confirming the system's effectiveness in real-time threat detection. However, the results showed no successful root logins, indicating that the security mechanisms in place, namely account lockouts and strong authentication protocols, prevent unauthorized access at higher privilege levels. This tool is integral for scaling and organization; as employee count and invested third-party companies increase, so do the potential vulnerable points.

By automating these processes, the tools significantly improved system monitoring efficiency, speed, and scalability. They allowed continuous oversight without human intervention and provided timely alerts for security breaches. This helps IT teams react to potential threats, while the data gathered from the inventory and brute-force detection systems ensures that the infrastructure remains secure and current.

Ultimately, these results highlight the importance of automation in maintaining a secure and efficient environment, proactively identifying threats, and optimizing system health across detection and inventory processes.

## References

Li, W., Leung, A., & Yue, W. (2023). Where is it in information security? The interrelationship among IT investment, security awareness, and data breaches. *MIS Quarterly, 47*, 317–342. https://doi.org/10.25300/misq/2022/15713

Schlackl, F., Link, N., & Hoehle, H. (2022). Antecedents and consequences of data breaches: A systematic review. *Information and Management, 59*, 103638. https://doi.org/10.1016/j.im.2022.103638

Woods, D. W., & Bohme, R. (2021). Systematization of knowledge: Quantifying cyber risk. *IEEE Symposium on Security and Privacy (S&P).*
