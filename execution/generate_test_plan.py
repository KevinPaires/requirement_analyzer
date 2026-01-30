#!/usr/bin/env python3
"""
Generate comprehensive Test Plan content based on requirement analysis.

This script takes a requirement specification and generates structured
test plan content following industry best practices.
"""

import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any


class TestPlanGenerator:
    """Generates test plan content from requirements."""

    def __init__(self, requirement: str, platform: str = "web",
                 project_name: str = "Project"):
        self.requirement = requirement
        self.platform = platform
        self.project_name = project_name

    def generate(self) -> Dict[str, Any]:
        """Generate complete test plan structure."""
        return {
            'document_control': self._generate_document_control(),
            'introduction': self._generate_introduction(),
            'scope': self._generate_scope(),
            'test_strategy': self._generate_test_strategy(),
            'test_environment': self._generate_test_environment(),
            'risk_analysis': self._generate_risk_analysis(),
            'test_deliverables': self._generate_test_deliverables(),
            'schedule': self._generate_schedule(),
            'roles_responsibilities': self._generate_roles()
        }

    def _generate_document_control(self) -> Dict[str, str]:
        """Generate document control section."""
        return {
            'document_name': f"{self.project_name} - Test Plan",
            'version': 'v1.0',
            'date_created': datetime.now().strftime('%Y-%m-%d'),
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'author': 'QA Team',
            'status': 'Draft'
        }

    def _generate_introduction(self) -> str:
        """Generate introduction and objectives."""
        return f"""
This test plan outlines the testing approach, strategy, and activities for: {self.requirement}

OBJECTIVES:
• Ensure the feature meets all functional requirements
• Validate non-functional requirements (performance, security, usability)
• Identify defects early in the development cycle
• Ensure the feature is production-ready
• Maintain quality standards and compliance
"""

    def _generate_scope(self) -> Dict[str, List[str]]:
        """Generate scope section."""
        # This is template-based - would be enhanced with AI analysis
        in_scope = [
            "Functional testing of all features",
            "Integration testing with existing systems",
            "Regression testing of related functionality",
            "UI/UX testing for {platform} platform".format(platform=self.platform),
            "Security testing (OWASP Top 10)",
            "Performance testing (response time, load handling)",
            "Accessibility testing (WCAG 2.1 AA compliance)",
            "Cross-browser/device compatibility testing"
        ]

        out_of_scope = [
            "Load testing beyond 1000 concurrent users",
            "Third-party service performance",
            "Infrastructure provisioning",
            "Production data migration (handled separately)"
        ]

        return {
            'in_scope': in_scope,
            'out_of_scope': out_of_scope
        }

    def _generate_test_strategy(self) -> Dict[str, Any]:
        """Generate test strategy section."""
        return {
            'testing_types': {
                'Functional Testing': 'Verify all features work as specified in requirements',
                'Integration Testing': 'Validate interactions between components and external systems',
                'Regression Testing': 'Ensure new changes do not break existing functionality',
                'Security Testing': 'Identify vulnerabilities (SQL injection, XSS, authentication bypass)',
                'Performance Testing': 'Measure response times, throughput, and resource usage',
                'Usability Testing': 'Evaluate user experience and interface intuitiveness',
                'Accessibility Testing': 'Ensure WCAG 2.1 AA compliance for users with disabilities'
            },
            'test_design_techniques': [
                'Equivalence Partitioning: Divide inputs into valid/invalid classes',
                'Boundary Value Analysis: Test min, max, and edge values',
                'Decision Table Testing: Cover all condition combinations',
                'State Transition Testing: Validate state changes',
                'Use Case Testing: Test real-world user scenarios',
                'Error Guessing: Apply experience to predict likely defects'
            ],
            'entry_criteria': [
                'Requirements documented and approved',
                'Test environment provisioned and accessible',
                'Test data prepared',
                'Code deployed to test environment',
                'Unit tests passing',
                'Smoke tests passing'
            ],
            'exit_criteria': [
                'All planned test cases executed',
                'Critical and High priority defects resolved',
                'Test coverage >= 95% of requirements',
                'Performance benchmarks met',
                'Security scan completed with no Critical findings',
                'Regression test suite passing',
                'Test summary report approved by stakeholders'
            ],
            'suspension_criteria': [
                'Critical defects blocking further testing',
                'Test environment unavailable for >4 hours',
                'Major requirement changes requiring test redesign',
                'Critical security vulnerability discovered'
            ],
            'resumption_criteria': [
                'Blocking defects fixed and verified',
                'Test environment restored and stable',
                'Updated requirements reviewed and test cases updated',
                'Security vulnerabilities patched'
            ]
        }

    def _generate_test_environment(self) -> Dict[str, Any]:
        """Generate test environment section."""
        environments = {
            'web': {
                'hardware': [
                    'Test server: 8 CPU cores, 16GB RAM',
                    'Database server: 4 CPU cores, 8GB RAM',
                    'Load balancer (if applicable)'
                ],
                'software': [
                    'Operating System: Ubuntu 22.04 LTS / Windows Server 2022',
                    'Web server: Nginx 1.24 / Apache 2.4',
                    'Database: PostgreSQL 15 / MySQL 8.0',
                    'Application runtime: Node.js 20 LTS / Python 3.11'
                ],
                'browsers': [
                    'Chrome (latest 2 versions)',
                    'Firefox (latest 2 versions)',
                    'Safari (latest version)',
                    'Edge (latest version)'
                ],
                'devices': [
                    'Desktop: 1920x1080, 1366x768',
                    'Tablet: iPad (768x1024), Android tablet',
                    'Mobile: iPhone 14, Samsung Galaxy S23'
                ]
            },
            'mobile': {
                'hardware': [
                    'iOS devices: iPhone 13, 14, 15',
                    'Android devices: Samsung Galaxy S22, S23, Google Pixel 7'
                ],
                'software': [
                    'iOS versions: 16.x, 17.x',
                    'Android versions: 12, 13, 14',
                    'API backend: [specify]'
                ]
            },
            'api': {
                'hardware': [
                    'API server: 4 CPU cores, 8GB RAM',
                    'Database server: 4 CPU cores, 8GB RAM'
                ],
                'software': [
                    'API framework: [specify]',
                    'Database: [specify]',
                    'Testing tools: Postman, Newman, JMeter'
                ]
            }
        }

        env = environments.get(self.platform, environments['web'])

        return {
            'hardware_requirements': env.get('hardware', []),
            'software_requirements': env.get('software', []),
            'test_data': [
                'Production-like dataset (anonymized)',
                'Edge case data (boundary values, special characters)',
                'Invalid data for negative testing',
                'Large datasets for performance testing'
            ],
            'browsers_devices': env.get('browsers', []) + env.get('devices', [])
        }

    def _generate_risk_analysis(self) -> Dict[str, List[str]]:
        """Generate risk analysis section."""
        return {
            'high_risk_areas': [
                'Authentication and authorization logic (security-critical)',
                'Payment processing (financial impact)',
                'Data validation and sanitization (SQL injection, XSS risk)',
                'Integration with third-party services (dependency risk)',
                'Database transactions (data integrity risk)',
                'Complex business logic with multiple conditions',
                'Recent code changes (high defect probability)'
            ],
            'mitigation_strategies': [
                'Increase test coverage for high-risk areas (>98%)',
                'Conduct security penetration testing',
                'Implement automated regression testing',
                'Perform code reviews for security-sensitive code',
                'Use static analysis tools (SonarQube, etc.)',
                'Conduct load testing to identify performance bottlenecks',
                'Implement monitoring and alerting in test environment',
                'Use staged rollout approach (canary deployment)'
            ]
        }

    def _generate_test_deliverables(self) -> List[str]:
        """Generate test deliverables section."""
        return [
            'Test Plan document (this document)',
            'Test Cases document with traceability matrix',
            'Exploratory Testing Charters',
            'Test Data preparation scripts',
            'Automated test scripts (if applicable)',
            'Test execution reports (daily/weekly)',
            'Defect reports with severity classification',
            'Performance test results',
            'Security scan reports',
            'Test summary report',
            'Test sign-off document'
        ]

    def _generate_schedule(self) -> Dict[str, str]:
        """Generate schedule and milestones."""
        today = datetime.now()

        return {
            'test_planning': f"{today.strftime('%Y-%m-%d')} - {(today + timedelta(days=2)).strftime('%Y-%m-%d')} (2 days)",
            'test_design': f"{(today + timedelta(days=3)).strftime('%Y-%m-%d')} - {(today + timedelta(days=7)).strftime('%Y-%m-%d')} (5 days)",
            'test_environment_setup': f"{(today + timedelta(days=3)).strftime('%Y-%m-%d')} - {(today + timedelta(days=5)).strftime('%Y-%m-%d')} (3 days)",
            'test_execution_functional': f"{(today + timedelta(days=8)).strftime('%Y-%m-%d')} - {(today + timedelta(days=15)).strftime('%Y-%m-%d')} (8 days)",
            'test_execution_integration': f"{(today + timedelta(days=16)).strftime('%Y-%m-%d')} - {(today + timedelta(days=19)).strftime('%Y-%m-%d')} (4 days)",
            'test_execution_regression': f"{(today + timedelta(days=20)).strftime('%Y-%m-%d')} - {(today + timedelta(days=22)).strftime('%Y-%m-%d')} (3 days)",
            'performance_security_testing': f"{(today + timedelta(days=23)).strftime('%Y-%m-%d')} - {(today + timedelta(days=25)).strftime('%Y-%m-%d')} (3 days)",
            'defect_retesting': f"{(today + timedelta(days=26)).strftime('%Y-%m-%d')} - {(today + timedelta(days=28)).strftime('%Y-%m-%d')} (3 days)",
            'test_reporting_closure': f"{(today + timedelta(days=29)).strftime('%Y-%m-%d')} - {(today + timedelta(days=30)).strftime('%Y-%m-%d')} (2 days)",
            'total_duration': '30 days'
        }

    def _generate_roles(self) -> Dict[str, str]:
        """Generate roles and responsibilities."""
        return {
            'QA Lead': 'Overall test strategy, team coordination, stakeholder communication, test plan approval',
            'QA Engineers': 'Test case design and execution, defect reporting, test data preparation, daily status updates',
            'Automation Engineers': 'Test automation framework, automated test script development, CI/CD integration',
            'Performance Engineers': 'Performance test design, load test execution, performance bottleneck analysis',
            'Security Testers': 'Security vulnerability assessment, penetration testing, OWASP Top 10 validation',
            'DevOps Engineers': 'Test environment provisioning, CI/CD pipeline maintenance, monitoring setup',
            'Business Analysts': 'Requirements clarification, test case review, UAT coordination',
            'Development Team': 'Defect fixing, unit test coverage, code review participation'
        }


def main():
    parser = argparse.ArgumentParser(
        description='Generate Test Plan content from requirement'
    )
    parser.add_argument('requirement', help='Requirement description')
    parser.add_argument('--platform', default='web',
                       choices=['web', 'mobile', 'api', 'desktop'],
                       help='Target platform')
    parser.add_argument('--project', default='Project',
                       help='Project name')
    parser.add_argument('--output', default=None,
                       help='Output JSON file (default: stdout)')

    args = parser.parse_args()

    generator = TestPlanGenerator(
        requirement=args.requirement,
        platform=args.platform,
        project_name=args.project
    )

    test_plan = generator.generate()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(test_plan, f, indent=2)
        print(f"Test plan saved to: {args.output}")
    else:
        print(json.dumps(test_plan, indent=2))


if __name__ == '__main__':
    main()
