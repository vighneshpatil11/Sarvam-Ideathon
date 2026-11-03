import type { Service } from "@/types";
// Illustrative records only. They contain no asserted government requirements or official links.
export const demoServices: Service[] = [
  { id: "demo-1", slug: "income-certificate", name: "Income Certificate", short_description: "Illustrative service entry. Connect the backend for authoritative information.", department_name: "Department information unavailable in demo", state: "Maharashtra", languages: ["en", "hi", "mr"], verification_status: "demo" },
  { id: "demo-2", slug: "domicile-certificate", name: "Domicile Certificate", short_description: "Illustrative service entry. Requirements and process are not verified in demo mode.", department_name: "Department information unavailable in demo", state: "Maharashtra", languages: ["en", "hi", "mr"], verification_status: "demo" },
  { id: "demo-3", slug: "student-scholarships", name: "Student Scholarships", short_description: "Illustrative category. Specific schemes and eligibility are not supplied in demo mode.", department_name: "Department information unavailable in demo", state: "Maharashtra", languages: ["en", "hi", "mr"], verification_status: "demo" }
];
